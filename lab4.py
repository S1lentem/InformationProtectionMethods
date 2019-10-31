from string import ascii_lowercase
from random import randint

from numbers import get_prime_nmber, get_prmitive_root
from logger import get_logger

LOGGER = get_logger('lab4', 'DEBUG')

def encrypt(msg, pub_key):
    b = randint(1, pub_key[0]-1)
    return [pow(pub_key[1], b, pub_key[0]), msg * pow(pub_key[2], b, pub_key[0]) % p]
   

def decrypt(c, secret_key):
    temp = pow(c[0], secret_key[0] - 1 - secret_key[1], secret_key[0])
    return (temp * c[1]) % secret_key[0]

if __name__ == '__main__':
    p = get_prime_nmber()                 
    g = get_prmitive_root(p)
    x = randint(1, p-1)   

    pub_key = [p, g, pow(g, x, p)]                   
    secret_key = [p, x]

    message = [ord(i) for i in 'BSUIR135']
    LOGGER.info('Message in numeric view: %s' % message)

    enc = [encrypt(item, pub_key) for item in message]
    LOGGER.info('Encypted message: %s' % enc)
    
    dec = [decrypt(i, secret_key) for i in enc]
    LOGGER.info('Decrypted message: %s' % dec)

    LOGGER.info('Message %s' % ''.join([chr(i) for i in dec]))
