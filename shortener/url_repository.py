import logging
import random
from retrying import retry
from sqlalchemy import create_engine, text, exc


def retry_if_integrity_error(exception):
    is_integrity_error = isinstance(exception, exc.IntegrityError)
    if is_integrity_error:
        logging.debug("IntegrityError detected, retrying")
    return is_integrity_error


class PostgresUrlRepository:
    def __init__(self, postgres_url):
        self.db = create_engine(postgres_url)
        self.stmts = {
            "add": text("insert into urls values (:id_, :url)"),
            "get": text("select url from urls where id = :id_"),
        }

    @retry(retry_on_exception=retry_if_integrity_error, stop_max_attempt_number=5)
    def add(self, url):
        # generate a random id up to the maximum int we can
        # hold in 8 characters (with 62 char alphabet)
        id_ = random.randint(0, 62 ** 8)
        self.db.execute(self.stmts["add"], {"id_": id_, "url": url})
        return id_

    def get(self, db_id):
        result = self.db.execute(self.stmts["get"], {"id_": db_id})
        row = result.fetchone()
        return row["url"]
