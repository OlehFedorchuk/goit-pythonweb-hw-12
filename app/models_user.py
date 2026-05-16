"""
User database model.

This module defines the User ORM model used by SQLAlchemy.
It represents application users and stores authentication and profile data.

Table:
    users

Fields:
    id (int): Primary key identifier.
    email (str): Unique user email address.
    username (str): Unique username.
    hashed_password (str): Securely hashed password.
    verified (bool): Email verification status.
    avatar (str | None): URL of user avatar image.
    role (str): User role ('user' or 'admin'). Default is 'user'.
"""

from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base


class User(Base):
    """
    User model representing application users.

    This model is used for authentication, authorization,
    and storing user profile information.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    verified = Column(Boolean, default=False)
    avatar = Column(String, nullable=True)
    role = Column(String, default="user")
