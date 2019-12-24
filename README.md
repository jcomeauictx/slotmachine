# slotmachine: gamble all day without leaving the house

simple Python3 script guesses keys for the top P2PKH addresses.

if you win, you are now a co-owner of that wallet and can spend the coins
as your own.

chances are infinitesimal, but if you win you win big: most of these wallets
have many millions of dollars in them, and some have billions.

requires ecdsa. as root, use `pip3 install ecdsa`, or on Debian and its
derivatives you can `apt install python3-ecdsa`.

to run, simply `make`, `./slotmachine.py`, or `python3 slotmachine.py`.

note: the chances that you guess the same private key as the original
address holder has are also infinitesimal: about 1 in 2^96 (a huge number:
79228162514264337593543950336), but since the hash matches, and you can
prove that, the coins are still counted as yours. note that **this is only
true** for funds held in P2PKH (Pay to Public Key Hash) transactions. for
P2PK (Pay to Public Key) transactions require a matching public key.

although everyone participating in Bitcoin should know the risks, many
don't, and will be furious with anyone "stealing" their coins this way.
plus, I don't expect the courts will get it right the first few cases
either. probably better just keep quiet about it if you win. treat it as
if you found a billion dollars in cash while walking down the street:
stuff it in your knapsack, shut up, and walk on nonchalantly.
