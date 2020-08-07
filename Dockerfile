FROM python:3.8-alpine

LABEL maintainer="Fred Campos <fred.tecnologia@gmail.com>"

RUN apk --update add --no-cache git sqlite-dev
RUN pip install poetry
RUN mkdir /app

WORKDIR /app

COPY pyproject.toml /app

RUN poetry install

COPY . /app
