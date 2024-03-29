#!/usr/bin/python3
r'''
base58 encoding and decoding

based on //github.com/jgarzik/python-bitcoinlib/blob/master/bitcoin/base58.py

test cases from https://tools.ietf.org/html/draft-msporny-base58-01

>>> encode(b'Hello World!')
b'2NEpo7TZRRrLZSi2U'

>>> encode(b'The quick brown fox jumps over the lazy dog.')
b'USm3fpXnKG5EUBx2ndxBDMPVciP5hGey2Jh4NDv6gmeo1LkMeiKrLJUUBk6Z'

the following test vector is modified from the erroneous original:

>>> encode(b'\x00\x00\x28\x7f\xb4\xcd')
b'11233QC4'

>>> decode(encode(b'\x00\x00\x28\x7f\xb4\xcd'))
b'\x00\x00(\x7f\xb4\xcd'
'''

from binascii import hexlify

DIGITS = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def encode(bytestring):
    '''
    base58 encoder

    differs from draft spec in that it converts entire bytestring to an
    integer all at one time instead of byte by byte. also does not use
    given variable names.
    '''
    padding = DIGITS[0:1] * (len(bytestring) - len(bytestring.lstrip(b'\0')))
    try:
        number = int.from_bytes(bytestring, 'big')
    except AttributeError:
        number = int(hexlify(bytestring), 16)
    encoded = b''
    while number:
        number, remainder = divmod(number, 58)
        encoded += DIGITS[remainder:remainder + 1]
    return bytes(padding + encoded[::-1])

def decode(bytestring):
    '''
    base58 decoder
    '''
    clean = bytestring.lstrip(DIGITS[0:1])
    padding = b'\0' * (len(bytestring) - len(clean))
    number = 0
    try:
        for byte in clean:
            number = (number * 58) + DIGITS.index(byte)
    except IndexError:
        raise ValueError('%r is not a base58 digit' % byte)
    # now convert to bytestring
    output = bytearray()
    while number:
        number, byte = divmod(number, 256)
        output.insert(0, byte)
    return bytes(padding + output)

def profile():
    '''
    for use with `make base58.profile`
    '''
    encode(b'\x00\x00\x28\x7f\xb4\xcd')

if bytes([65]) != b'A':  # python2
    # pylint: disable=redefined-builtin, invalid-name
    class bytes(str):
        '''
        fake `bytes` class to make doctests pass
        '''
        def __new__(cls, initial=''):
            if isinstance(initial, list):
                joined = ''.join(map(chr, initial))
                return super(bytes, cls).__new__(cls, joined)
            return super(bytes, cls).__new__(cls, initial)
        def __repr__(self):
            return 'b' + super(bytes, self).__repr__()
        __str__ = __repr__
