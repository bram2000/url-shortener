import logging
import validators
from flask import jsonify, request, redirect, url_for


class UrlShortener:
    def __init__(self, flask_app, url_repository, codec):
        self.flask_app = flask_app
        self.url_repository = url_repository
        self.codec = codec
        self._configure_routes()

    def _configure_routes(self):
        logging.debug("Configuring flask routes")
        self.flask_app.add_url_rule(
            "/shorten_url", "shorten", self.shorten, methods=["POST"]
        )
        self.flask_app.add_url_rule("/<key>", "lookup", self.lookup, methods=["GET"])

    def shorten(self):
        logging.debug("----> shorten_url")
        if not request.json:
            return error_response("No json payload found")

        url = request.json.get("url")
        if not url:
            return error_response("No url found")

        logging.info("Shortening url %s", url)

        if not validators.url(url):
            return error_response("url failed validation")

        row_id = self.url_repository.add(url)
        key = self.codec.encode(row_id)

        shortened_url = url_for("lookup", _external=True, key=key)
        logging.debug("shortened_url: %s", shortened_url)

        response = jsonify({"shortened_url": shortened_url})
        response.status_code = 201

        return response

    def lookup(self, key):
        db_id = self.codec.decode(key)
        url = self.url_repository.get(db_id)
        if not url:
            return error_response("no url found")

        logging.info("redirecting to %s", url)

        return redirect(url, code=301)


def error_response(message):
    logging.warning("error: %s", message)
    response = jsonify({"error": message})
    response.status_code = 400
    return response
