.PHONY: test

test:
	pytest . --cov=coartintator --cov-report=term-missing --cov-report=html


coverage:
	open htmlcov/index.html