venv_name := .venv
sources := apt_preferences test

help:
	@echo "lint - check style with ruff"
	@echo "format - format style with black and isort"
	@echo "tests - run tests quickly with pytest"
	@echo "venv - creates virtual environment"
	@echo "install - install requirements"
	@echo "install-dev - install dev requirements"
	@echo "clean - remove venv"	
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-git - remove ignored and not ignored files"

lint:
	python -m ruff $(sources)
	python -m mypy $(sources)

format:
	python -m black $(sources)
	python -m isort $(sources)

tests:
	python -m pytest -vv

venv:
	clean-venv: rm -rf $(venv_name)


install: 
	pip install -e .

install-dev: 
	pip install -e .[DEV]

clean-venv: rm -rf $(venv_name)

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

clean-git:
	git clean -fxd