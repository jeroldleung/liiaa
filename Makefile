.PHONY: build run dev prod format

IMAGE_NAME = liiaa

build:
		@docker build -t $(IMAGE_NAME) .

run:
		@docker run -d -p 8000:8000 $(IMAGE_NAME)

dev:
		@uv run uvicorn app:app --reload

prod:
		@uv run uvicorn app:app --host 0.0.0.0 --port 8000

format:
		@uv tool run ruff format .
		@uv tool run ruff check --fix .