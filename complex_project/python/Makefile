.PHONY: *

#################################################################
# Shared variables
#################################################################

PACKAGE_DIR_ML=bootcamp_2021_01

#################################################################
# help
#################################################################

help:
	@echo "#####################################"
	@echo "# Setting UP the Python environment #"
	@echo "#####################################"
	@echo ""
	@echo "\tsetup-env-full: Install all dependencies required for every part of this project"
	@echo ""
	@echo "All other target starting with 'setup-env' will install parts of these dependencies"
	@echo "required for some specific part of the project (ml, dash, running tests, jupyter)."
	@echo ""
	@echo "#######################"
	@echo "# Docker image Docker #"
	@echo "#######################"
	@echo ""
	@echo "All these docker goals will be base on the same firsts layers to optimize build time."
	@echo ""
	@echo "For all docker targets, you should provide a 'TAG' environment variable"
	@echo "\tdocker-build: Build Docker image"
	@echo "\tdocker-build-dash: Build Docker image for running Dash"
	@echo ""
	@echo "###############"
	@echo "# Development #"
	@echo "###############"
	@echo ""
	@echo "\trun-local: Run local Dash application"
	@echo "\tnotebook: Run jupyter notebook"
	@echo "\trepl: Run a Python REPL"
	@echo "\ttest: Run unit tests"
	@echo "\tlint: Run a linter on the code"
	@echo "\tformat: Format file according to PEP-8"
	@echo "\tformat-check: Check file formatting (non-zero return code if format is wrong)"
	@echo "\ttype: Check typing"


#################################################################
# setting up dev env
#################################################################

upgrade-pip:
	poetry run pip install --upgrade pip

setup-dev-host:
	./scripts/install_pyenv.sh
	./scripts/install_poetry.sh
	@echo "Host setup correctly. Restart your shell or source your shell config file to be up and running :)"

setup-env-common: clean upgrade-pip
	poetry install --no-root --no-dev

setup-env-dev: setup-env-common
	poetry install -E test -E bdd -E type -E format -E lint -E repl --no-root

setup-env-ml: setup-env-common
	poetry install -E ml --no-root --no-dev

setup-env-dash: setup-env-common
	poetry install -E dash --no-root --no-dev

setup-env-jupyter: setup-env-common
	poetry install -E notebook --no-root
	poetry run jupyter contrib nbextension install --user
	poetry run jupyter nbextension enable toc2/main
	poetry run jupyter nbextension enable varInspector/main
	poetry run jupyter nbextension enable execute_time/ExecuteTime
	poetry run jupyter nbextension enable hide_input/main
	poetry run jupyter nbextension enable hide_input_all/main
	poetry run jupyter nbextension enable init_cell/main
	poetry run jupyter nbextension enable collapsible_headings/main
	poetry run jupyter nbextension enable notify/notify
	poetry run jupyter nbextension enable splitcell/splitcell
	poetry run jupyter nbextension enable toggle_all_line_numbers/main

setup-env-full: setup-env-dev setup-env-ml setup-env-dash setup-env-jupyter

setup-pre-commit-hooks:
	pre-commit install --hook-type pre-commit

#################################################################
# cleaning
#################################################################

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

clean-venv:
	# poetry env remove might not to work if `virtualenvs.in-project = true`
	# (see https://github.com/python-poetry/poetry/issues/2124)
	# so if not, remove whole `.venv` directory using https://unix.stackexchange.com/questions/153763
	poetry env remove $$(poetry env info -p)/bin/python && ([ $$? -eq 0 ]) || rm -rf $$(poetry env info -p)


#################################################################
# docker
#################################################################

docker-build: --check-tag
	docker build -f Dockerfile -t ekinoxio/bootcamp-2021-01:$${TAG} .

docker-build-dash: --check-tag
	docker build -f Dockerfile.dash -t ekinoxio/bootcamp-2021-01-dash:$${TAG} .

docker-build-test: --check-tag
	docker build -f Dockerfile.tests -t ekinoxio/bootcamp-2021-01-tests:$${TAG} .

--check-tag:
ifndef TAG
	$(error "You must declare TAG environment variable. \
	TAG defines the tag of the Docker image.")
endif

#################################################################
# Run Local
#################################################################

run-local:
	poetry run python -m bootcamp_2021_01.gui.ekilibr8

#################################################################
# notebook
#################################################################

notebook:
ifdef ENV
	poetry run jupyter notebook --NotebookApp.token=$$ENV --NotebookApp.ip='*'
else
	poetry run jupyter notebook
endif

#################################################################
# unit testing
#################################################################

test:
	poetry run python -c "import sys; import pytest; sys.argv = ['']; sys.exit(pytest.main())"

#################################################################
# linting
#################################################################

lint:
	poetry run flake8 $(PACKAGE_DIR_ML) tests

#################################################################
# formating
#################################################################

seed-isort:
	poetry run seed-isort-config

isort:
	poetry run isort -rc $(PACKAGE_DIR_ML) tests -vb

black:
	poetry run black $(PACKAGE_DIR_ML) tests

format: seed-isort isort black

format-check:
	poetry run isort -c -rc $(PACKAGE_DIR_ML) tests -vb
	poetry run black --check $(PACKAGE_DIR_ML) tests

#################################################################
# typing
#################################################################

type:
	poetry run mypy -p $(PACKAGE_DIR_ML) -p tests

#################################################################
# repl
#################################################################

repl:
	poetry run bpython

#################################################################
# git targets
#################################################################

prune-branches:
	git remote prune origin
	git branch -vv | grep ': gone]'|  grep -v "\*" | awk '{ print $$1; }' | xargs git branch -d

prune-branches-force:
	git remote prune origin
	git branch -vv | grep ': gone]'|  grep -v "\*" | awk '{ print $$1; }' | xargs git branch -D

pbf: prune-branches-force

post-PR-merge-sync-step-1:
	git switch master
	git pull

post-PR-merge-sync: post-PR-merge-sync-step-1 prune-branches-force

pms: post-PR-merge-sync
