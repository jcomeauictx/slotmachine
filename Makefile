RICHLIST := blockchair_bitcoin_addresses_latest.tsv.gz
RICHLIST_URL := https://gz.blockchair.com/bitcoin/addresses/$(RICHLIST)
RICHLIST_PATH := $(shell echo ~/Downloads)/$(RICHLIST)
RICHLIST_TXT ?= $(RICHLIST_PATH:.tsv.gz=.txt)
SCRIPTS := $(wildcard *.py)
export
run:
	$(MAKE) RICHLIST_TXT= slots
slots: slotmachine.py $(RICHLIST_TXT)
	./$<
%.pylint: %.py
	pylint3 $<
%.test:	%.py
	python3 -m doctest $<
%.profile: %.py
	python3 -c "import cProfile, $*; \
	 cProfile.run('$@()')"
tests:	$(SCRIPTS:.py=.test)
profile: $(SCRIPTS:.py=.profile)
lint:	$(SCRIPTS:.py=.pylint)
https://gz.blockchair.com/bitcoin/addresses/blockchair_bitcoin_addresses_latest.tsv.gz
check: tests lint profile
env:
	env
$(RICHLIST_PATH): .FORCE
	cd $(@D) && wget -c -N $(RICHLIST_URL) || true
$(RICHLIST_TXT): $(RICHLIST_PATH)
	zcat $< | awk '$$1 ~ /^1/ && $$2 ~ /......*/ {print $$1 " " $$2}' > $@
.FORCE:
