#!/usr/bin/python3
'''
try and find keys for some of the richest Bitcoin wallets

made from table contents copied-and-pasted from 99bitcoins.com/bitcoin/rich-list
awk '$2 ~ /^1/ {print $2}' /tmp/richlist.txt > richlist.txt

if you find a winner you can import the privkey into your wallet
'''
#pylint: disable=multiple-imports
from __future__ import print_function
import sys, hashlib, logging, secrets
import ecdsa
logging.basicConfig(level=logging.DEBUG if __debug__ else logging.INFO)

BASE58_DIGITS = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def spin(secret=None, richlist=None, maxreps=None):
    '''
    try and guess private keys for some of the richest BTC addresses

    >>> spin('satoshi nakamoto', ['1Q7f2rL2irjpvsKVys5W2cmKJYss82rNCy'])
    JACKPOT!
    seed: satoshi nakamoto
    secret: aa2d3c4a4ae6559e9f13f093cc6e32459c5249da723de810651b4b54373385e2
    private key: 5K7EWwEuJu9wPi4q7HmWQ7xgv8GxZ2KqkFbjYMGvTCXmY22oCbr
    address: 1Q7f2rL2irjpvsKVys5W2cmKJYss82rNCy
    reps: 1
    '''
    if not richlist:
        with open('richlist.txt') as infile:
            richlist = infile.read().split()
    seed = secret
    try:
        maxreps = int(maxreps)  # will fail if None
    except TypeError:
        maxreps = sys.maxsize  # continue indefinitely
    try:
        if len(secret) != 64:
            raise TypeError('not a sha256 hash')
        secret = bytes.fromhex(secret)
    except TypeError:
        logging.warning('converting "%s" to sha256 hexdigest first', secret)
        try:
            secret = sha256(secret.encode())
        except (TypeError, AttributeError) as problem:
            logging.warning('cannot sha256sum %s: %s', secret, problem)
            logging.info('creating random secret instead')
            secret = secrets.token_bytes(32)
    old_secret, private, address, reps = None, None, None, 0
    while address not in richlist and reps < maxreps:
        print('secret: %s' % secret.hex(), file=sys.stderr)
        private = wifkey(secret)
        address = wifaddress(public_key(secret))
        old_secret, secret = secret, sha256(secret)
        reps += 1
    if address in richlist:
        print('JACKPOT!')
        print('seed: %s' % seed)
        print('secret: %s' % old_secret.hex())
        print('private key: %s' % private)
        print('address: %s' % address)
        print('reps: %s' % reps)

def public_key(secret):
    '''
    `secret` must be 256 bit string
    '''
    signing_key = ecdsa.SigningKey.from_string(secret, curve=ecdsa.SECP256k1)
    verifying_key = signing_key.verifying_key
    return b'\x04' + verifying_key.to_string()

def wifkey(key, prefix=b'\x80'):
    '''
    return key in Wallet Import Format

    prefix b'\x80' is for private key, '\x00' for public key
    '''
    bytestring = prefix + key
    checksum = sha256(sha256(bytestring))[:4]
    return base58encode(bytestring + checksum).decode('ascii')

def wifaddress(publickey):
    '''
    return public key hash in Wallet Import Format (WIF)
    '''
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(sha256(publickey))
    return wifkey(ripemd160.digest(), b'\x00')

def sha256(data):
    '''
    sha256 hash of data
    '''
    return hashlib.sha256(data).digest()

def base58encode(bytestring):
    '''
    simple base58 encoder

    based on //github.com/jgarzik/python-bitcoinlib/blob/master/
     bitcoin/base58.py
    '''
    encoded = ''
    cleaned = bytestring.lstrip(b'\0')
    number = int.from_bytes(bytestring, 'big')
    while number:
        number, remainder = divmod(number, 58)
        encoded += BASE58_DIGITS[remainder]
    padding = BASE58_DIGITS[0] * (len(bytestring) - len(cleaned))
    return (padding + encoded[::-1]).encode()

if __name__ == '__main__':
    print(spin(*sys.argv[1:]))
