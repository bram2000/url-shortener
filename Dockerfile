FROM python:3.7.1-alpine3.8

RUN apk --update upgrade && apk add \
    build-base \
    gcc \
    python3 \
    python3-dev \
    postgresql-dev

RUN pip3 install alembic psycopg2-binary

COPY . /opt/shortener
WORKDIR /opt/shortener
RUN pip3 install -e .

CMD ["url_shortener"]
