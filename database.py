# shorter_app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import get_settings

# The engine is the entry point of the databse
engine = create_engine(
    get_settings().db_url,
    
    # With this connection argument SQLite allows for more than one request at a time to communicate with the database
    connect_args = {"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()