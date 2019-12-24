SCRIPTS := $(wildcard *.py)
run:	slotmachine.py
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
check: tests lint profile
