.PHONY: dev format

dev:
		@uvicorn app:app --reload

format:
		@uvx ruff format .
		@uvx ruff check --fix .