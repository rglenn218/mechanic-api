import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import quote_plus

try:
    from dotenv import load_dotenv
    
    BASE_DIR = Path(__file__).resolve().parent
    load_dotenv(BASE_DIR / ".env")
except ImportError:
    pass

class Config:
    password = quote_plus(os.getenv("MYSQL_PASSWORD"))
    
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://"
        f"{os.getenv('MYSQL_USER')}:"
        f"{password}@"
        f"{os.getenv('MYSQL_HOST')}:"
        f"{os.getenv('MYSQL_PORT')}/"
        f"{os.getenv('MYSQL_DATABASE')}"
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 60
    
class TestingConfig(Config):
    TESTING = True
    
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://"
        f"{os.getenv('MYSQL_USER')}:"
        f"{Config.password}@"
        f"{os.getenv('MYSQL_HOST')}:"
        f"{os.getenv('MYSQL_PORT')}/"
        f"mechanic_test_db"
    )
    
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SECRET_KEY = os.getenv("SECRET_KEY")
    
    if not SQLALCHEMY_DATABASE_URI:
        raise RuntimeError("DATABASE_URI was not loaded from the environment.")