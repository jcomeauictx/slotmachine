#!/usr/bin/python3
'''
partial secrets module for Python3 before version 3.6

just the parts we need for slotmachine
'''
import random
from binascii import unhexlify

GENERATOR = random.SystemRandom()

def python3_token_bytes(number):
    '''
    return random bytestring
    '''
    return GENERATOR.getrandbits(number * 8).to_bytes(number, 'big')

def python2_token_bytes(number):
    '''
    return random bytestring
    '''
    token = GENERATOR.getrandbits(number * 8)
    try:
        return unhexlify('%0*x' % (number * 2, token))
    except TypeError:
        raise ValueError(
            'Failed to unhexlify %d byte "%0*x"' % (number, number, token)
        )

def profile():
    '''
    for `make profile`
    '''
# pylint: disable=invalid-name  # don't force ALL_CAPS on method name
try:
    python3_token_bytes(32)
    token_bytes = python3_token_bytes
except AttributeError:
    token_bytes = python2_token_bytes
