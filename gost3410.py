from os import urandom
from md5 import md5

from codecs import getdecoder
from codecs import getencoder

from logger import get_logger
from rsa import extended_gcd

LOGGER = get_logger('gost3410', 'INFO')

MODE_TO_SIZE = {
    2001: 32,
    2012: 64,
}

PARAMS = (
        getdecoder("hex")("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFD97")[0],
        getdecoder("hex")("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF6C611070995AD10045841B09B761B893")[0],
        getdecoder("hex")("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFD94")[0],
        getdecoder("hex")("00000000000000000000000000000000000000000000000000000000000000a6")[0],
        getdecoder("hex")("0000000000000000000000000000000000000000000000000000000000000001")[0],
        getdecoder("hex")("8D91E471E0989CDA27DF505A453F2B7635294F2DDF23E3B122ACC99C9E9F1E14")[0],
)

def bytes_to_long(raw):
    return int(getencoder("hex")(raw)[0].decode("ascii"), 16)


def long_to_bytes(n, size=32):
    LOGGER.debug('Long to bytes n: %s' % n)
    
    res = hex(int(n))[2:].rstrip("L")
    if len(res) % 2 != 0:
        res = "0" + res
    s = getdecoder("hex")(res)[0]
    if len(s) != size:
        s = (size - len(s)) * b"\x00" + s
    return s


def modinvert(a, n):
    if a < 0:
        return n - modinvert(-a, n)
    
    t, newt = 0, 1
    r, newr = n, a
    
    while newr != 0:
        quotinent = r // newr
        t, newt = newt, t - quotinent * newt
        r, newr = newr, r - quotinent * newr
    
    if r > 1:
        return -1
    
    if t < 0:
        t = t + n
    return t




class GOST3410Curve(object):
    def __init__(self, p, q, a, b, x, y):
        self.p = bytes_to_long(p)
        self.q = bytes_to_long(q)
        self.a = bytes_to_long(a)
        self.b = bytes_to_long(b)
        self.x = bytes_to_long(x)
        self.y = bytes_to_long(y)


    def _pos(self, v):
        return v + self.p if v < 0 else v
    

    def __add(self, p1x, p1y, p2x, p2y):
        if p1x == p2x and p1y == p2y:
            t = ((3 * p1x * p1x + self.a) * modinvert(2 * p1y, self.p)) % self.p
        else:
            tx = self._pos(p2x - p1x) % self.p
            ty = self._pos(p2y - p1y) % self.p
            t = (ty * modinvert(tx, self.p)) % self.p
        tx = self._pos(t * t - p1x - p2x) % self.p
        ty = self._pos(t * (p1x - tx) - p1y) % self.p
        LOGGER.debug('tx) %s; ty) %s' % (tx, ty))

        return tx, ty

    def exp(self, degree, x=None, y=None):
        x = x or self.x
        y = y or self.y
        tx, ty = x, y
        degree -= 1
       
        while degree != 0:
            if degree & 1 == 1:
                tx, ty = self.__add(tx, ty, x, y)
            degree = degree >> 1
            x, y = self.__add(x, y, x, y)
        LOGGER.debug('tx) %s; ty) %s' % (tx, ty))

        return tx, ty


def public_key(curve, prv):
    return curve.exp(prv)


def sign(curve, prv, digest, mode=2001):
    LOGGER.debug('digest %s ' % digest)
    if type(digest) is str:
        digest = digest.encode('utf-8')

    size = MODE_TO_SIZE[mode]
    q = curve.q
    e = bytes_to_long(digest) % q
    e = e or 1

    while True:
        k = bytes_to_long(urandom(size)) % q
        if k == 0:
            continue
        r, _ = curve.exp(k)
        r %= q
        if r == 0:
            continue
        d = prv * r
        k *= e
        s = (d + k) % q
        if s == 0:
            continue
        break
    return long_to_bytes(s, size) + long_to_bytes(r, size)


def verify(curve, pub, digest, signature, mode=2001):
    if type(digest) is str:
        digest = digest.encode('utf-8')

    size = MODE_TO_SIZE[mode]
    
    q = curve.q
    p = curve.p
    s = bytes_to_long(signature[:size])
    r = bytes_to_long(signature[size:])
    if r <= 0 or r >= q or s <= 0 or s >= q:
        return False
    e = bytes_to_long(digest) % curve.q
    if e == 0:
        e = 1
    v = modinvert(e, q)
    z1 = s * v % q
    z2 = q - r * v % q
    p1x, p1y = curve.exp(z1)
    q1x, q1y = curve.exp(z2, pub[0], pub[1])
    lm = q1x - p1x
    if lm < 0:
        lm += p
    lm = modinvert(lm, p)
    z1 = q1y - p1y
    lm = lm * z1 % p
    lm = lm * lm % p
    lm = lm - p1x - q1x
    lm = lm % p
    if lm < 0:
        lm += p
    lm %= q

    return lm == r


def prv_unmarshal(prv):
    
    return bytes_to_long(prv[::-1])

if __name__ == '__main__':
    data = 'BSUR135'.encode('utf-8')
    data2 = 'BSUIR_NOT_135'.encode('utf-8')

    p, q, a, b, x, y = PARAMS
    curve = GOST3410Curve(p, q, a, b, x, y)
    prv = prv_unmarshal(urandom(32))
    result = sign(curve, prv, md5(data))
    
    pub = public_key(curve, prv)

    is_success = verify(curve, pub, md5(data), result)
    LOGGER.info('Input) %s; data2) %s; result) %s' % (data.decode('utf-8'), data.decode('utf-8'), is_success))

    is_fail = verify(curve, pub, md5(data2), result)
    LOGGER.info('Input) %s; data2) %s; result) %s' % (data.decode('utf-8'), data2.decode('utf-8'), is_fail))