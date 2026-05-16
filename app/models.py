"""
Contact database model.

This module defines the Contact ORM model used by SQLAlchemy.
It represents user-owned contacts stored in the application.

Table:
    contacts

Relationships:
    - Many-to-one relationship with User (owner of contacts)
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Contact(Base):
    """
    Contact model representing a user's contact entry.

    Each contact belongs to a specific user and stores personal
    information such as name, email, phone, and birthday.
    """

    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    birthday = Column(String)
    additional_data = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User")