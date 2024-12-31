.PHONY: build run dev test prod lint clean

IMAGE_NAME = liiaa

build:
		@docker build -t $(IMAGE_NAME) .

run:
		@docker run -d -p 8000:8000 $(IMAGE_NAME)

dev:
		@uv run uvicorn app.main:app --reload

test:
		@uv run pytest tests

prod:
		@uv run uvicorn app.main:app --host 0.0.0.0 --port 8000

lint:
		@uv run ruff format .
		@uv run ruff check --fix .
		@uv run mypy app tests

clean:
		@find ./app | grep __pycache__ | xargs rm -rf