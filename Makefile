.PHONY: install test lint format up down psql status

install:
	pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check src tests

format:
	ruff check src tests --fix

up:
	docker compose up -d postgres

down:
	docker compose down

psql:
	docker exec -it fund_finance_postgres psql -U fundfinance -d fundfinance

status:
	git status

.PHONY: demo
demo:
	./scripts/demo_workflow.sh

.PHONY: preflight
preflight:
	./scripts/preflight_check.sh
