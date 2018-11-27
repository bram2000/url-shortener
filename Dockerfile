FROM python:3.7.1-alpine3.8

ADD https://github.com/just-containers/s6-overlay/releases/download/v1.21.7.0/s6-overlay-x86.tar.gz /tmp/
RUN tar xzf /tmp/s6-overlay-x86.tar.gz -C /

ENTRYPOINT ["/init"]

RUN apk --update upgrade && apk add \
    build-base \
    gcc \
    python3 \
    python3-dev \
    postgresql-dev

RUN pip3 install alembic psycopg2-binary

COPY ./docker/root /
COPY . /opt/shortener
WORKDIR /opt/shortener
RUN pip3 install -e .
