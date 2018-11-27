import validators


class UrlShortener:
    def __init__(self, url_repository, codec):
        self.url_repository = url_repository
        self.codec = codec

    def url_to_key(self, url):
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
