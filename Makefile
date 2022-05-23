.DEFAULT_GOAL = default
default: clean format lint coverage

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


.PHONY: clean
clean: ## Remove all build, test, coverage and Python artifacts
	rm -fr build dist .eggs *egg-info .tox/ .cache/ .pytest_cache/ docs/_build/ .coverage htmlcov +
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

.PHONY: poetry
poetry: ## Install poetry
	poetry install
	poetry shell

.PHONY: format
format: ## Format files
	# Sort imports one per line, so autoflake can remove unused imports
	poetry run isort --force-single-line-imports app tests сор
	poetry run autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place app --exclude=__init__.py
	poetry run black app tests
	poetry run isort app tests


.PHONY: lint
lint: ## Lint files
	poetry run mypy --show-error-codes app
	poetry run flake8
	poetry run bandit app
	poetry run safety check

.PHONY: pre-commit
pre-commit: ## Format & lint before commit
	poetry run pre-commit run --all-file

.PHONY: test
test: ## Test
	poetry run pytest

.PHONY: coverage
coverage: ## Test coverage
	poetry run pytest --cov=app --cov-report=term-missing --cov-report xml tests

.PHONY: run-dev
run-dev: ## Run the local development server
	poetry run uvicorn app.main:app --reload --lifespan on --workers 1 --host 0.0.0.0 --port 8080 --log-level debug

.PHONY: run
run: ## Run the local server
	uvicorn app.main:app --lifespan on --workers 1 --host 0.0.0.0 --port 8080