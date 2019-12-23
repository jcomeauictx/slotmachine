run:	slotmachine.py
	./$<
lint:	slotmachine.py
	pylint3 $<
test:	slotmachine.py
	python3 -m doctest $<
