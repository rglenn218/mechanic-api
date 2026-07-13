import os 

from application import create_app
from config import ProductionConfig

if not os.getenv("DATABASE_URI"):
    raise RuntimeError("DATABASE_URI environment variable is required.")

if not os.getenv("SECRET_KEY"):
    raise RuntimeError("SECRET_KEY environment variable is required.")

app = create_app(ProductionConfig)