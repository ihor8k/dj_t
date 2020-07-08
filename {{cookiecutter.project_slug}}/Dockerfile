FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE config.settings
ENV ROOT_DIR /usr/src

WORKDIR $ROOT_DIR

RUN set -ex \
    && addgroup -g 82 -S www-data \
    && adduser -u 82 -D -S -G www-data www-data \
    && apk add --upgrade --no-cache --virtual .build-deps \
        openssl-dev \
    && apk add --upgrade --virtual \
        build-base \
        gcc \
        libffi-dev \
        libc-dev \
        postgresql-dev \
        python3-dev \
        jpeg-dev \
        zlib-dev \
    && apk --no-cache add --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing watchman

COPY . $ROOT_DIR

RUN set -ex \
    && pip install --upgrade pip \
    && pip install -r $ROOT_DIR/requirements.txt --no-cache-dir \
    && apk del --no-cache .build-deps \
    && chown -R www-data:www-data $ROOT_DIR
