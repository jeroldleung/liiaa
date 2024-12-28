FROM python:3.12-slim

# specify the working directory to /app
WORKDIR /app

# copy the application into the container or the working directory
COPY ./app ./app

# using uv temporarily to install the application dependencies
COPY pyproject.toml .
RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
    uv pip install --system --no-cache -r pyproject.toml

# run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
