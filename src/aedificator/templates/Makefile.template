RM := rm -rf
SHELL := /bin/bash

.PHONY: clean clean-pyc clean-test clean-shared clean-build distclean

clean: clean-pyc clean-test clean-shared clean-build

venv:
	@python3 -m venv .venv
	@source .venv/bin/activate && python -m pip install -U pip flit tox
	@echo "Ready to develop - type source .venv/bin/activate in your terminal!"

develop:
	flit install --symlink

clean-pyc:
	find . -name '*.pyc' -type f -exec $(RM) '{}' +
	find . -name '__pycache__' -type d -exec $(RM) '{}' +

clean-test:
	$(RM) .coverage
	$(RM) .mypy_cache
	$(RM) .pytest_cache
	$(RM) .hypothesis
	$(RM) .tox

clean-build:
	$(RM) build
	$(RM) dist
	find . -name '*.egg-info' -exec $(RM) '{}' +
	find . -name '*.egg' -exec $(RM) '{}' +
	find . -name '.eggs' -exec $(RM) '{}' +

clean-shared:
	find $(DIRS_TO_CLEAN) -name '*.so' -type f -exec $(RM) '{}' +

distclean: clean
	$(RM) .venv
