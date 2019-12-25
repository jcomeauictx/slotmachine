#!/usr/bin/python3
'''
partial secrets module for Python3 before version 3.6

just the parts we need for slotmachine
'''
import random

def token_bytes(number):
    '''
    return random bytestring
    '''
    generator = random.SystemRandom()
    return generator.getrandbits(number * 8).to_bytes(number, 'big')
