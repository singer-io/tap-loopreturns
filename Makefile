.DEFAULT_GOAL := test

test:
	pylint tap_loopreturns -d missing-docstring
	nosetests tests
