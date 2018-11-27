import logging
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
            return self.error_response("No json payload found")

        url = request.json.get("url")
        if not url:
            return self.error_response("No url found")

        logging.info("Shortening url %s", url)

        try:
            key = self.url_shortener.url_to_key(url)
        except ValueError as error:
            return self.error_response(str(error))

        shortened_url = url_for("lookup", _external=True, key=key)
        logging.debug("Shortened url: %s", shortened_url)

        response = jsonify({"shortened_url": shortened_url})
        response.status_code = 201
        return response

    def lookup(self, key):
        try:
            url = self.url_shortener.key_to_url(key)
        except Exception as error:
            return self.error_response(str(error), 404)
        logging.info("Redirecting to %s", url)
        return redirect(url, code=301)

    def error_response(self, message, status_code=400):
        logging.warning("error: %s", message)
        response = jsonify({"error": message})
        response.status_code = status_code
        return response
