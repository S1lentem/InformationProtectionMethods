from logger import get_logger
from md5 import md5

LOGGER = get_logger('HMAC', 'DEBUG')

trans_5C = bytes((x ^ 0x5C) for x in range(256))
trans_36 = bytes((x ^ 0x36) for x in range(256))

def hmac(key, data, block_size=64):
    if len(key) > block_size:
        key = hash(key).digest()

    LOGGER.debug('Key) %s' % key)
    key = key.ljust(block_size, '0')
    LOGGER.debug('Key) %s' % key)
    
    k_ipad = ''.join([chr(ord(x) ^ y) for x, y in zip(key, trans_5C)])
    LOGGER.debug('k_i) %s' % k_ipad)

    k_opad = ''.join([chr(ord(x) ^ y) for x, y in zip(key, trans_36)])
    LOGGER.debug('k_o) %s' % k_opad)

    return md5(k_opad.encode('utf-8') + md5(k_ipad.encode('utf-8') + data).encode('utf-8'))

if __name__ == '__main__':
    data = 'BSUR135'.encode('utf-8')

    res = hmac('12345678', data)
    LOGGER.info('Result) %s' % res)