.PHONY: dev format

dev:
		@uv run fastapi dev

format:
		@uvx ruff format .
		@uvx ruff check --fix .