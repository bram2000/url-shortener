import string
import dozen


class AppConfig(dozen.Template):
    db_host: str = "localhost"
    db_user: str = "postgres"
    db_password: str = "postgres"
    db_name: str = "shortener"

    app_host: str = "0.0.0.0"
    app_port: int = 5000

    alphabet: str = string.digits + string.ascii_letters

    loglevel: str = "INFO"


_CONFIG = AppConfig().build()


def get_postgres_url():
    host = _CONFIG.db_host
    user = _CONFIG.db_user
    password = _CONFIG.db_password
    name = _CONFIG.db_name
    return f"postgresql://{user}:{password}@{host}/{name}"


def get_app_host():
    return _CONFIG.app_host


def get_app_port():
    return _CONFIG.app_port


def get_loglevel():
    return _CONFIG.loglevel


def get_alphabet():
    return _CONFIG.alphabet
