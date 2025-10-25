SHELL := /bin/bash


PY_MODULE := cli_template
PY_SCRIPT := .venv/bin/cli-template  # from 'console_scripts' in setup.cfg
PY_FILES  := $(shell find $(PY_MODULE) -type f -name '*.py')

.PHONY: default
default: test $(PY_SCRIPT)

.PHONY: all
all: update default


$(PY_SCRIPT): .venv requirements.txt pyproject.toml setup.cfg setup.py $(PY_FILES)
	.venv/bin/pip3 install .


.venv: /usr/bin/python3
	/usr/bin/python3 -m venv --clear .venv
	@make update


.PHONY: test
test: .venv
	.venv/bin/tox -e pep8	


.PHONY: update
update: .venv requirements.txt test-requirements.txt
	.venv/bin/pip3 install --upgrade --upgrade-strategy eager -r requirements.txt
	.venv/bin/pip3 install --upgrade --upgrade-strategy eager -r test-requirements.txt


.PHONY: clean
clean:
	rm -rf .tox .venv *.egg-info
