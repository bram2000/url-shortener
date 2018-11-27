# Composition root for dependency injection
import logging
from flask import Flask
from .url_repository import PostgresUrlRepository
from .codec import Codec
from .app import UrlShortener
from . import config

logging.basicConfig(level=config.get_loglevel())

FLASK = Flask(__name__)
REPOSITORY = PostgresUrlRepository(config.get_postgres_url())
CODEC = Codec(config.get_alphabet())

APP = UrlShortener(FLASK, REPOSITORY, CODEC)
FLASK.run(host=config.get_app_host(), port=config.get_app_port())
