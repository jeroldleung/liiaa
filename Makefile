.PHONY: lint

lint:
		ruff format
		ruff check --fix

test:
		pytest tests
