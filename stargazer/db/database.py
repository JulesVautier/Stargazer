import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

"""
    Improvements: use a config manager to handle this, like Dynaconf
"""

POSTGRES_USER = os.environ.get("POSTGRES_USER", "stargazer")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "stargazer")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "stargazer")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", 5432)
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
