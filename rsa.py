import random

from numbers import get_prime_nmber, gcd
from logger import get_logger

LOGGER = get_logger('RSA', 'DEBUG')

def extended_gcd(a, b):
    x, y, lx, ly = 0, 1, 1, 0
    oa = a
    ob = b
    while b != 0:   
        q = a // b
        (a, b) = (b, a % b)
        (x, lx) = ((lx - (q * x)), x)
        (y, ly) = ((ly - (q * y)), y)
    if lx < 0:
        lx += ob
    if ly < 0:
        ly += oa
    return a, lx, ly


def find_p_q():
    p, q = get_prime_nmber(1000), None

    while q is None or p == q:
        q = get_prime_nmber(1000)

    return max(p, q), min(p, q)


def generate_keypair(p, q):
    n = p * q

    phi = (p-1) * (q-1)

    while True:
        e = random.randrange(1, phi)
        if gcd(e, phi) == 1:
            break

    d = extended_gcd(e, phi)[1]
    
    return ((e, n), (d, n))


def encrypt(pk, plaintext):
    e, n = pk
    cipher = [(ord(char) ** e) % n for char in plaintext]

    return cipher


def decrypt(pk, ciphertext):
    d, n = pk
    plain = [chr((char ** d) % n) for char in ciphertext]

    return ''.join(plain)
    

if __name__ == '__main__':
    message = 'BSUIR135'
    LOGGER.info('message: %s' % message)
    
    p, q = find_p_q()
    public, private = generate_keypair(p, q)
    
    LOGGER.info('public key: %s| private key: %s' % (public, private))

    encrypted_msg = encrypt(private, message)
    LOGGER.info("Encrypted message: %s " % ' '.join(map(lambda x: hex(x), encrypted_msg)))

    LOGGER.info('decypted message: %s' % decrypt(public, encrypted_msg))