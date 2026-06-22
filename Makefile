.PHONY: help up down logs test lint typecheck format check

help:
	@echo "up         - start app + postgres (docker compose)"
	@echo "down       - stop and remove containers"
	@echo "logs       - tail app logs"
	@echo "test       - run pytest"
	@echo "lint       - ruff check"
	@echo "typecheck  - mypy"
	@echo "format     - ruff format"
	@echo "check      - lint + typecheck + test"

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