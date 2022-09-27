# syntax=docker/dockerfile:1

FROM python:3.9-alpine
WORKDIR /python-docker

COPY requirements.txt requirements.txt

RUN apk add build-base && \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    python -m pip install "pymongo[srv]" && \
    apk --purge del .build-deps

COPY . .

ENV APP_SETTINGS="config.Config"
ENV SQLALCHEMY_DATABASE_URI="postgresql://postgres:postgres@patternfi_db:5432/patternfi"
ENV SQLALCHEMY_DATABASE_URI_TEST="postgresql://postgres:postgres@patternfi_db:5432/patternfi_test"

CMD ["gunicorn", "-b", "0.0.0.0:8000", "wsgi:application"]