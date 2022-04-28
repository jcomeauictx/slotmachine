# slotmachine: gamble all day without leaving the house

simple Python3 script guesses keys for the top P2PKH addresses.

if you win, you are now a co-owner of that wallet and can spend the coins
as your own.

## quickstart

requires ecdsa. as root, use `pip3 install ecdsa`, or on Debian and its
derivatives you can `apt install python3-ecdsa`.

to run, simply `make`, `./slotmachine.py`, or `python3 slotmachine.py`.

## notes on odds

chances are infinitesimal, but if you win you win big: most of these wallets
have many millions of dollars in them, and some have billions.

note: even if you guessed a key that generates the wallet address,
the chances that you guessed the same private key as the original
address holder are also infinitesimal: about 1 in 2^96 (a huge number:
79228162514264337593543950336), but since the hash matches, and you can
prove that, the coins are still counted as yours. note that **this is only
true** for funds held in P2PKH (Pay to Public Key Hash) transactions. for
P2PK (Pay to Public Key) transactions you instead need a matching public key.
for reference, see [Chris Moore](https://twitter.com/dooglus)'s [comments on
this Bitcoin question](https://bitcoin.stackexchange.com/questions/22/is-it-possible-to-brute-force-bitcoin-address-creation-in-order-to-steal-money).

put another way, you have one chance in 2^160, or 1 in
1461501637330902918203684832716283019655932542976, of scoring any one of
the wallet addresses, but only one chance in 2^256, or 1 in
115792089237316195423570985008687907853269984665640564039457584007913129639936,
of getting that address's original public/private key pair.

## legality

although everyone participating in Bitcoin should know the risks, many
don't, and will be furious with anyone "stealing" their coins this way.
plus, I don't expect the courts will get it right the first few cases
either. probably better just keep quiet about it if you win. treat it as
if you found a billion dollars in cash while walking down the street:
stuff it in your knapsack, shut up, and walk on nonchalantly.

## richlist.txt

a better source of addresses may be <https://gz.blockchair.com/bitcoin/addresses/blockchair_bitcoin_addresses_latest.tsv.gz>, updated weekly. you can use
this list automatically by using `make slots` instead of just `make`. it takes
longer to load, however.

## notes for Windows Vista

may be helpful for other versions of windows as well...

you will need to get ecdsa from the webpage at <https://pypi.org/project/ecdsa/#files>, unless you can get pip installed (I could not). you should be able to
`tar xvf ecdsa-0.17.0.tar.gz` and `python setup.py` in the resulting directory to install the module.

## notes for Android/Termux

once you fix your sources.list using termux-change-repo to A1batross, you should be able to install python (which is really python3). if you `make PYLINT=echo PY_VER= fast`, you should get through the first few snags, but then it fails on using the ripemd160 hash.

## notes for Debian wheezy

pip doesn't work, or at least I couldn't get it to work: using `--index-url https://pypi.python.org/simple` fails without telling you why, but if you look in `$HOME/.pip/pip.log` you'll see `HTTP Error 403: SNI is required`.

so, you have to fetch both `six` and `ecdsa` from pypi.org with a browser, as mentioned above under Windows Vista, and install them in that order. then it will run using `PY_VER=2 PYLINT=echo make fast`.
