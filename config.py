import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

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