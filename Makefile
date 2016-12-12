all: test

test:
	PYTHONPATH=.:$PYTHONPATH pylint -E --load-plugins oops_overrides_checker tests/fixtures/my_naive_code.py
