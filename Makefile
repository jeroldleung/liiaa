.PHONY: build run dev prod lint clean

IMAGE_NAME = liiaa

build:
		@docker build -t $(IMAGE_NAME) .

run:
		@docker run -d -p 8000:8000 $(IMAGE_NAME)

dev:
		@uv run uvicorn app.main:app --reload

prod:
		@uv run uvicorn app.main:app --host 0.0.0.0 --port 8000

lint:
		@uv tool run ruff format .
		@uv tool run ruff check --fix .

clean:
		@rm -rf **/__pycache__