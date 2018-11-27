# Composition root for dependency injection
import logging
from flask import Flask
from .url_shortener import UrlShortener
from .url_repository import PostgresUrlRepository
from .codec import Codec
from .app import WebService
from . import config


logging.basicConfig(
    format="[%(asctime)s %(name)s %(levelname)s] %(message)s",
    level=config.get_loglevel(),
)

FLASK = Flask(__name__)
REPOSITORY = PostgresUrlRepository(config.get_postgres_url())
CODEC = Codec(config.get_alphabet())
SHORTENER = UrlShortener(REPOSITORY, CODEC)
APP = WebService(FLASK, SHORTENER)
FLASK.run(host=config.get_app_host(), port=config.get_app_port())
