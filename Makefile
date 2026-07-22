.PHONY: help up down logs test lint typecheck format check migrate revision

help:
	@echo "up         - start app + postgres (docker compose)"
	@echo "down       - stop and remove containers"
	@echo "logs       - tail app logs"
	@echo "test       - run pytest"
	@echo "lint       - ruff check"
	@echo "typecheck  - mypy"
	@echo "format     - ruff format"
	@echo "check      - lint + typecheck + test"
	@echo "fix        - ruff check and fix"

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f app

test:
	uv run pytest

lint:
	uv run ruff check .

typecheck:
	uv run mypy .

format:
	uv run ruff format .

check: lint typecheck test

fix:
	uv run ruff check . --fix

migrate:
	uv run alembic upgrade head

revision:
	uv run alembic revision --autogenerate -m "$(m)"