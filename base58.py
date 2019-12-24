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

>>> encode(0x0000287fb4cd.to_bytes(6, 'big'))
b'11233QC4'

>>> decode(encode(0x0000287fb4cd.to_bytes(6, 'big')))
0x0000287fb4cd
'''
DIGITS = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def encode(bytestring):
    '''
    base58 encoder

    differs from draft spec in that it converts entire bytestring to an
    integer all at one time instead of byte by byte. also does not use
    given variable names.
    '''
    padding = DIGITS[0:1] * (len(bytestring) - len(bytestring.lstrip(b'\0')))
    number = int.from_bytes(bytestring, 'big')
    encoded = b''
    while number:
        number, remainder = divmod(number, 58)
        encoded += DIGITS[remainder:remainder + 1]
    return padding + encoded[::-1]

def decode(bytestring):
    '''
    base58 decoder
    '''
    raw_bytes = bytearray(b'')
    try:
        for index in range(len(bytestring)):
            carry = DIGITS.index(bytestring[index])
            for offset in range(index + 1, len(bytestring)):
                if not carry:
                    break
                else:
                    carry += DIGITS.index(bytestring[offset]) * 58
                    carry, byte = divmod(carry, 256)
                    raw_bytes.append(byte)
    except IndexError:
        raise ValueError('%r is not a base58 digit' % bytestring[0])
    return bytes(raw_bytes)
