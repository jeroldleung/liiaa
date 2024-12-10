.PHONY: dev format

dev:
		@uvicorn app.main:app --reload

format:
		@uvx ruff format .
		@uvx ruff check --fix .