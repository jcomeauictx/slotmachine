SHELL := /bin/bash
RICHLIST := blockchair_bitcoin_addresses_latest.tsv.gz
RICHLIST_URL := https://gz.blockchair.com/bitcoin/addresses/$(RICHLIST)
RICHLIST_PATH := $(shell echo ~/Downloads)/$(RICHLIST)
RICHLIST_TXT ?= $(RICHLIST_PATH:.tsv.gz=.txt)
SCRIPTS := $(wildcard *.py)
# script uses about 100MB per million addresses, set limit accordingly
MAX_ADDRESSES ?= 4000000
# `make OPTIMIZE=-00 run` to get maximum CPU (no wasted screen I/O)
OPTIMIZE ?=
PYTHON ?= python3 $(OPTIMIZE)

export
run:
	$(MAKE) RICHLIST_TXT= slots
slots: slotmachine.py $(RICHLIST_TXT)
	$(PYTHON) $<
%.pylint: %.py
	pylint3 $<
%.test:	%.py
	python3 -m doctest $<
%.profile: %.py
	RICHLIST_TXT= python3 -OO -c "import cProfile, $*; \
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
recreate: $(RICHLIST_PATH)
	touch $<
$(RICHLIST_TXT): $(RICHLIST_PATH)
	zcat $< | awk '$$1 ~ /^1/ && $$2 ~ /..*/ {print $$1 " " $$2}' > $@
%/Downloads: %
	mkdir $@
python:  # run python3 with environment as set by Makefile
	python3 -OO -i -c "from slotmachine import *"
%.try:  # test a key for 1000 reps
	try=$*; python3 -OO slotmachine.py "$${try//_/ }" "" 1000
.FORCE:
