"""
Database configuration module.

This module initializes the SQLAlchemy engine, session factory,
and base class for ORM models. It also provides a dependency
for database session management in FastAPI.

Environment Variables:
    DATABASE_URL (str): Database connection URL.

Example:
    postgresql://user:password@localhost:5432/dbname
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from os import getenv
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()


def get_db():
    """
    Dependency that provides a database session.

    This function is used with FastAPI's Depends system.
    It creates a new database session for each request and
    ensures it is properly closed after use.

    Yields:
        Session: SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()