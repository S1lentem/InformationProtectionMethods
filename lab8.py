import os, sys, argparse

from logger import get_logger

TEXT_FILE_NAME = 'text.txt'
DECODED_TEXT_FILE_NAME = 'decoded.txt'
IMG_FILE_NAME = 'img.bmp'
ENCODED_IMG_FILE_NAME = 'encoded.bmp'

DECODE_CHOISE = 'decode'
ENCODE_CHOISE = 'encode'

LOGGER = get_logger('stgraph', 'INFO')

parser = argparse.ArgumentParser()
parser.add_argument('-t', action='store', dest='type')
parser.add_argument('-d', action='store', dest='degree',  type=int)
parser.add_argument('-r', action='store', dest='to_read', type=int)

def create_mask(degree):
    text_mask = 0b11111111
    img_mask = 0b11111111

    text_mask <<= (8 // degree)
    text_mask %= 256
    img_mask >>= degree
    img_mask <<= degree

    return text_mask, img_mask



def decrypt(degree, to_read):
    img_len = os.stat(ENCODED_IMG_FILE_NAME).st_size

    if to_read >= img_len * degree /8 - 54:
        print('To long text')
        return

    text = open(DECODED_TEXT_FILE_NAME, 'w')
    encoded_bmp = open(ENCODED_IMG_FILE_NAME, 'rb')

    encoded_bmp.seek(54)
    
    _, img_mask = create_mask(degree)
    img_mask = ~img_mask

    read = 0
    while read < to_read:
        symbol = 0

        for _ in range(0, 8, degree):
            img_byte = int.from_bytes(encoded_bmp.read(1), sys.byteorder) & img_mask
            symbol <<= degree
            symbol |= img_byte

        read += 1
        text.write(chr(symbol))

    text.close()
    encoded_bmp.close()


def encrypt(degree):
    text_len = os.stat(TEXT_FILE_NAME).st_size
    img_len = os.stat(IMG_FILE_NAME).st_size

    if text_len >= img_len/8 - 54:
        print('To long text')
        return

    text = open(TEXT_FILE_NAME, 'r')
    start_bmp = open(IMG_FILE_NAME, 'rb')
    encoded_bmp = open(ENCODED_IMG_FILE_NAME, 'wb')

    encoded_bmp.write(start_bmp.read(54))

    text_mask, img_mask = create_mask(degree)

    while True:
        symbol = text.read(1)
        
        if not symbol:
            break

        symbol = ord(symbol)
        for _ in range(0, 8, degree):
            img_byte = int.from_bytes(start_bmp.read(1), sys.byteorder) & img_mask
            bits = symbol & text_mask
            bits >>= (8 - degree) 

            img_byte |= bits
            encoded_bmp.write(img_byte.to_bytes(1, sys.byteorder))
            symbol <<= degree

    start_bmp.tell()

    encoded_bmp.write(start_bmp.read())

    text.close()
    start_bmp.close()
    encoded_bmp.close()
    
if __name__ == '__main__':
    args = parser.parse_args()
    choise = args.type
    degree = args.degree

    LOGGER.info('CHOISE - %s' % choise)
    LOGGER.info('DEGREE - %s' % degree)

    if choise == ENCODE_CHOISE:
        encrypt(degree)
        LOGGER.info('enctipting success')
    elif choise == DECODE_CHOISE:
        LOGGER.info('TO READ - %s' % args.to_read)
        decrypt(degree, args.to_read)
        LOGGER.info('decripting succsess')
    else:
        print('Invlid type')