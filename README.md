# slotmachine: gamble all day without leaving the house

simple Python3 script guesses keys for the top P2PKH addresses.

if you win, you are now a co-owner of that wallet and can spend the coins
as your own.

chances are infinitesimal, but if you win you win big: most of these wallets
have many millions of dollars in them.

requires ecdsa and base58. as root, use `pip3 install base58` and
`pip3 install ecdsa`, or on Debian and its derivatives you can
`apt install python3-base58 python3-ecdsa`.

to run, simply `make`, `./slotmachine.py`, or `python3 slotmachine.py`.
