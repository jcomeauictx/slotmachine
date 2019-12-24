run:	slotmachine.py
	./$<
lint:	slotmachine.py
	pylint3 $<
test:	slotmachine.py
	python3 -m doctest $<
profile:
	python3 -c "import cProfile, slotmachine; \
	 cProfile.run('slotmachine.spin(None, None, 10)')"
