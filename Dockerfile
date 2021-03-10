# Build image
FROM python:3.9-alpine AS build-image

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apk add --no-cache gcc gcc musl-dev python3-dev libffi-dev openssl-dev cargo

RUN pip install -U pip

COPY poetry.lock pyproject.toml ./

ARG ENVIRONMENT=${ENVIRONMENT}

RUN pip install poetry==1.1.4 && \
    poetry config virtualenvs.in-project true && \
    poetry install $(test "$ENVIRONMENT" == production && echo "--no-dev") --no-interaction --no-ansi

# Runtime image
FROM python:3.9-alpine AS runtime-image

EXPOSE 8000

WORKDIR /app

COPY --from=build-image /app/.venv/ /app/.venv/

COPY . /app

CMD  .venv/bin/uvicorn --host=0.0.0.0 app.main:app
