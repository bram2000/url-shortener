import logging
import validators
from flask import jsonify, request, redirect, url_for


class WebService:
    def __init__(self, flask_app, url_shortener):
        self.flask_app = flask_app
        self.url_shortener = url_shortener
        self._configure_routes()

    def _configure_routes(self):
        logging.debug("Configuring flask routes")
        self.flask_app.add_url_rule(
            "/shorten_url", "shorten", self.shorten, methods=["POST"]
        )
        self.flask_app.add_url_rule("/<key>", "lookup", self.lookup, methods=["GET"])

    def shorten(self):
        if not request.json:
            return error_response("No json payload found")

        url = request.json.get("url")
        if not url:
            return error_response("No url found")

        logging.info("Shortening url %s", url)

        try:
            key = url_shortener.url_to_key(url)
        except Exception as error:
            return self.error_response(error.message)

        shortened_url = url_for("lookup", _external=True, key=key)
        logging.debug("Shortened url: %s", shortened_url)

        response = jsonify({"shortened_url": shortened_url})
        response.status_code = 201
        return response

    def lookup(self, key):
        try:
            url = self.url_shortener.key_to_url(key)
        except Exception as error:
            return self.error_response(error.message, 404)

        logging.info("Redirecting to %s", url)

        return redirect(url, code=301)

    def error_response(message, status_code=400):
        logging.warning("error: %s", message)
        response = jsonify({"error": message})
        response.status_code = status_code
        return response


class UrlShortener:
    def __init__(self, url_repository, codec):
        self.url_repository = url_repository
        self.codec = codec

    def url_to_key(self):
        if not validators.url(url):
            raise ValueError("url failed validation")
        row_id = self.url_repository.add(url)
        key = self.codec.encode(row_id)
        return key

    def key_to_url(self, key):
        db_id = self.codec.decode(key)
        try:
            url = self.url_repository.get(db_id)
        except KeyError:
            raise ValueError("url not found")
        return url
