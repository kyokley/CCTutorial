ARG BASE_IMAGE=python:3.10-slim

FROM ${BASE_IMAGE} AS base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt-get update && apt-get install -y g++

RUN pip install -U pip

ENV POETRY_VENV=/poetry_venv
RUN python3 -m venv $POETRY_VENV

ENV VIRTUAL_ENV=/venv
RUN python3 -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH:$POETRY_VENV/bin"

RUN $POETRY_VENV/bin/pip install poetry

COPY poetry.lock pyproject.toml /code/

RUN $POETRY_VENV/bin/poetry install

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
