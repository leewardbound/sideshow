export PIPENV_VERBOSITY=-1

# Dev utilities
dev:
	make deps
	bin/dc up -d
	bin/dc ps

deps:
	make venv
	make docker_build
	make generate
	make frontend_deps

frontend_deps:
	cd sideshow/views && yarn

docker_build:
	bin/dc build

docker_build_clean:
	bin/dc build --no-cache

generate:
	.venv/bin/python3 sideshow/cli.py generate-enums

format:
	make ruff_format
	make black
	make isort
	make autoflake
	make mypy

venv:
	uv venv .venv
	. .venv/bin/activate ; uv pip install -e .

precommit:
	make format
	make generate
	make test

# CI Pipeline & Tests

test:
	pytest

test_backend_coverage:
	pytest --cov=sideshow/apps --cov-config=.coveragerc --cov-report html --cov-report term
	echo "View coverage report: file://${PWD}/htmlcov/index.html"

# Data management & Backups
dump_fixtures:
	bin/djmanage dumpdata --natural-primary --natural-foreign --format json --indent 2 users

# Codebase Linting & Cleanup

clean:
	find . -name '*.pyc' -delete

mypy:
	mypy

isort:
	isort sideshow

flake8:
	flake8

autoflake:
	autoflake -r -i --expand-star-imports --remove-all-unused-imports --remove-duplicate-keys --remove-unused-variables --ignore-init-module-imports sideshow/apps/

black:
	black sideshow wsgi.py manage.py

ruff_check:
	ruff check .

ruff_format:
	ruff format .
