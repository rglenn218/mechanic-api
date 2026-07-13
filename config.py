import os
from pathlib import Path
from urllib.parse import quote_plus

try:
    from dotenv import load_dotenv

    BASE_DIR = Path(__file__).resolve().parent
    load_dotenv(BASE_DIR / ".env")
except ImportError:
    pass


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 60


class DevelopmentConfig(Config):
    password = quote_plus(os.getenv("MYSQL_PASSWORD", ""))

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://"
        f"{os.getenv('MYSQL_USER', 'root')}:"
        f"{password}@"
        f"{os.getenv('MYSQL_HOST', '127.0.0.1')}:"
        f"{os.getenv('MYSQL_PORT', '3306')}/"
        f"{os.getenv('MYSQL_DATABASE', 'mechanic_db')}"
    )


class TestingConfig(Config):
    TESTING = True

    password = quote_plus(os.getenv("MYSQL_PASSWORD", "testpassword"))

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://"
        f"{os.getenv('MYSQL_USER', 'root')}:"
        f"{password}@"
        f"{os.getenv('MYSQL_HOST', '127.0.0.1')}:"
        f"{os.getenv('MYSQL_PORT', '3306')}/"
        f"mechanic_test_db"
    )


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SECRET_KEY = os.getenv("SECRET_KEY")