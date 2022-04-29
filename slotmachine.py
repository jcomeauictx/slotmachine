#!/usr/bin/python3 -OO
'''
try and find keys for some of the richest Bitcoin wallets

made from table contents copied-and-pasted from 99bitcoins.com/bitcoin/rich-list
awk '$2 ~ /^1/ {print $2}' /tmp/richlist.txt > richlist.txt

if you find a winner you can import the privkey into your wallet
'''
#pylint: disable=multiple-imports
from __future__ import print_function
import sys, os, hashlib, logging
import ecdsa, base58
logging.basicConfig(
    level=logging.DEBUG if __debug__ else logging.INFO,
    format='%(levelname)s:%(message)s'
)
try:
    import secrets
except ImportError:  # Python3 before 3.6
    logging.info('using monkeypatch to provide `secrets` services')
    import monkeypatch_secrets as secrets
try:
    import signal, termios
except ImportError as problem:
    logging.info('cannot make use of ^T status readout: %s', problem)
    signal = termios = None
if hasattr(bytes, 'hex'):
    #pylint: disable=invalid-name
    hexlify = lambda bytestring: bytestring.hex()
    unhexlify = bytes.fromhex
else:
    import binascii
    #pylint: disable=invalid-name
    hexlify = lambda bytestring: binascii.hexlify(bytestring).decode()
    unhexlify = binascii.unhexlify

RICHLIST = os.getenv('RICHLIST_TXT') or 'richlist.txt'
MAX_ADDRESSES = int(os.getenv('MAX_ADDRESSES', '0')) or 4000000
MIN_SATOSHIS = int(os.getenv('MIN_SATOSHIS', '0')) or 10000

def spin(secret=None, richlist=None, maxreps=None, fake_success=False):
    '''
    try and guess private keys for some of the richest BTC addresses

    >>> spin('satoshi nakamoto', ['1Q7f2rL2irjpvsKVys5W2cmKJYss82rNCy'], 1)
    JACKPOT!
    seed: 'satoshi nakamoto'
    secret: aa2d3c4a4ae6559e9f13f093cc6e32459c5249da723de810651b4b54373385e2
    private key: 5K7EWwEuJu9wPi4q7HmWQ7xgv8GxZ2KqkFbjYMGvTCXmY22oCbr
    address: 1Q7f2rL2irjpvsKVys5W2cmKJYss82rNCy
    reps: 1
    '''
    # pylint: disable=too-many-locals, too-many-branches, too-many-statements
    if not richlist:
        with open(RICHLIST) as infile:
            richlist = []
            logging.info('building richlist')
            for line in infile:
                data = line.split()
                if len(data) > 1 and int(data[1]) < MIN_SATOSHIS:
                    logging.info('cutting off at value %s', data[1])
                    break
                else:
                    logging.debug('data: %s', data)
                    richlist.append(data[0])
                if len(richlist) == MAX_ADDRESSES:  # watch memory usage
                    logging.info('cutting off at %d addresses', len(richlist))
                    break
            logging.info('done building richlist, %d addresses', len(richlist))
        richlist = dict.fromkeys(richlist)  # for faster lookups
    seed = secret or None  # specifying blank on command line means random seed
    try:
        maxreps = int(maxreps)  # will fail if None
    except TypeError:
        logging.warning('cannot convert %r to integer', maxreps)
        logging.info('program will run until exited with ^C')
        maxreps = sys.maxsize  # continue indefinitely
    try:
        if len(secret) != 64:
            raise TypeError('Not a sha256 hash')
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
    # trap ^T to show current guess count, overriding ^\ "quit"
    if termios is not None:
        terminal_attributes = termios.tcgetattr(sys.stdin)
        quit_character = terminal_attributes[-1][termios.VQUIT]
        def control(character):
            if ord(character) >= 0x20:  # space character
                return chr(ord(character) & 0x1f).encode()
            return chr(ord(character) | 0x20)
        def trap_control_t():
            terminal_attributes[-1][termios.VQUIT] = control('T')
            termios.tcsetattr(sys.stdin, termios.TCSANOW, terminal_attributes)
            signal.signal(signal.SIGQUIT, quit_handler)
        def quit_handler(number=None, stack=None):
            logging.debug('signal number: %s, stack: %s', number, stack)
            print('\nguesses so far: %d' % reps, file=sys.stderr)
    try:
        if termios is not None and not __debug__:
            logging.info('^T will show how many guesses made so far')
            trap_control_t()
        logging.info('starting guessing secrets, ^C to quit')
        while address not in richlist and reps < maxreps:
            logging.debug('secret: %s', hexlify(secret))
            private = wifkey(secret)
            address = wifaddress(public_key(secret))
            old_secret = secret
            # if we aren't starting from a chosen seed, randomize each new try
            # otherwise keep deriving it from the seed
            secret = secrets.token_bytes(32) if seed is None else sha256(secret)
            reps += 1
        if address in richlist or fake_success:
            print('JACKPOT!')
            print('seed: %r' % seed)
            print('secret: %s' % hexlify(old_secret))
            print('private key: %s' % private)
            print('address: %s' % address)
            print('reps: %s' % reps)
    except KeyboardInterrupt:
        print('\nexiting, total %d guesses made' % reps, file=sys.stderr)
        print('total attempts (guesses * %d addresses)): %d' %
              (len(richlist), reps * len(richlist)), file=sys.stderr)
    finally:
        if termios is not None:
            logging.info('setting terminal I/O back to defaults')
            terminal_attributes[-1][termios.VQUIT] = quit_character
            termios.tcsetattr(sys.stdin, termios.TCSANOW, terminal_attributes)
            signal.signal(signal.SIGQUIT, signal.SIG_DFL)

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
    return base58.encode(bytestring + checksum).decode('ascii')

def wifaddress(publickey):
    '''
    return public key hash in Wallet Import Format (WIF)
    '''
    try:
        hashed = hashlib.new('ripemd160', sha256(publickey)).digest()
    except ValueError:  # assume "unsupported hash type"
        from Crypto.Hash import RIPEMD
        hashed = RIPEMD.new(sha256(publickey)).digest()
    logging.debug('hashed: %r', hashed)
    return wifkey(hashed, b'\x00')

def sha256(data):
    '''
    sha256 hash of data
    '''
    return hashlib.sha256(data).digest()

def profile():
    '''
    for running profiler with `make profile`
    '''
    spin(None, None, 10)

if __name__ == '__main__':
    print(spin(*sys.argv[1:]))
