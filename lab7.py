from codecs import getdecoder

from logger import get_logger
from gost3410 import bytes_to_long, long_to_bytes, MODE_TO_SIZE, modinvert

LOGGER = get_logger('lab7', 'INFO')

CURVE_PARAMS =  (
        getdecoder("hex")("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFD97")[0],
        getdecoder("hex")("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFD94")[0],
        getdecoder("hex")("00000000000000000000000000000000000000000000000000000000000000a6")[0],
)

class Curve(object):
    def __init__(self, p, a, b):
        self.p = bytes_to_long(p)
        self.a = bytes_to_long(a)
        self.b = bytes_to_long(b)
        

    def _pos(self, v):
        return v + self.p if v < 0 else v
    

    def _add(self, p1x, p1y, p2x, p2y):
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
        tx, ty = x, y
        degree -= 1
        while degree != 0:
            if degree & 1 == 1:
                tx, ty = self._add(tx, ty, x, y)
            degree = degree >> 1
            x, y = self._add(x, y, x, y)
        LOGGER.debug('tx) %s; ty) %s' % (tx, ty))
        
        return tx, ty

if __name__ == '__main__':
    curve = Curve(*CURVE_PARAMS)

    d_a = 123123
    d_b = 432123
    G = (123123, 12312311)

    H_a = curve.exp(d_a, *G)
    H_b = curve.exp(d_b, *G)

    secret_a = curve.exp(d_a, *H_b)
    secret_b  = curve.exp(d_b, *H_a)

    LOGGER.info('First')
    LOGGER.info('Public - %s', H_a)
    LOGGER.info('Private - %s', secret_a)
    
    LOGGER.info('Second')
    LOGGER.info('Public - %s', H_b)
    LOGGER.info('Private - %s', secret_b)
   
    LOGGER.info('Equal secrets %s' % (secret_a == secret_b)) 
    