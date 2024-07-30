FROM python:3.11-slim-buster

ENV TZ=Europe/Moscow
ENV POETRY_VERSION=1.5.1
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_NO_CACHE_DIR=off
ENV PYTHONDONTWRITEBYTECODE=on
ENV PYTHONFAULTHANDLER=on
ENV PYTHONUNBUFFERED=on
ENV PYTHONPATH=src

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -yq --no-install-recommends \
    build-essential curl && rm -rf /var/lib/apt/lists/*
RUN pip install "poetry==$POETRY_VERSION" && poetry config virtualenvs.create false

WORKDIR app/
COPY alembic.ini ./
COPY . ./
RUN poetry install --no-interaction --no-ansi -vvv
