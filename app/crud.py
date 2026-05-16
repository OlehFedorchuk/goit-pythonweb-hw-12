"""
CRUD operations for contacts and users.

This module provides database operations for creating, reading, updating,
and deleting contacts and user data. All functions follow a consistent pattern
of accepting a database session and returning the result or None if not found.

Functions:
    create_contact: Create a new contact for a user.
    get_contacts: Retrieve all contacts for a user with optional filters.
    get_contact_by_id: Get a specific contact by ID.
    update_contact: Update contact information.
    delete_contact: Delete a contact.
    get_upcoming_birthdays: Get contacts with birthdays in the next 7 days.
    get_user_by_email: Retrieve user by email address.
    get_user_by_id: Retrieve user by ID.
"""

from sqlalchemy.orm import Session
from app.models import Contact
from datetime import date, timedelta, datetime

from app.models_user import User


def create_contact(db: Session, contact, user_id):
    """
    Create a new contact for a specific user.

    Args:
        db (Session): SQLAlchemy database session.
        contact: Pydantic schema containing contact data.
        user_id (int): ID of the user who owns the contact.

    Returns:
        Contact: The created contact object.
    """
    obj = Contact(**contact.model_dump(), user_id=user_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_contacts(db, user_id, first_name=None, last_name=None, email=None):
    """
    Retrieve all contacts for a user with optional filtering.

    Args:
        db (Session): Database session.
        user_id (int): Owner of contacts.
        first_name (str, optional): Filter by first name.
        last_name (str, optional): Filter by last name.
        email (str, optional): Filter by email.

    Returns:
        list[Contact]: List of matching contacts.
    """
    query = db.query(Contact).filter(Contact.user_id == user_id)

    if first_name:
        query = query.filter(Contact.first_name.ilike(f"%{first_name}%"))

    if last_name:
        query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))

    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))

    return query.all()


def get_contact_by_id(db, contact_id, user_id):
    """
    Retrieve a single contact by ID for a specific user.

    Args:
        db (Session): Database session.
        contact_id (int): Contact ID.
        user_id (int): Owner of contact.

    Returns:
        Contact | None: Contact object if found, otherwise None.
    """
    return db.query(Contact).filter(
        Contact.id == contact_id,
        Contact.user_id == user_id
    ).first()


def update_contact(db, contact_id, data, user_id):
    """
    Update an existing contact.

    Args:
        db (Session): Database session.
        contact_id (int): ID of contact to update.
        data: Pydantic schema with updated fields.
        user_id (int): Owner of contact (for security).

    Returns:
        Contact | None: Updated contact or None if not found.
    """
    contact = db.query(Contact).filter(
        Contact.id == contact_id,
        Contact.user_id == user_id
    ).first()

    if contact:
        contact.first_name = data.first_name
        contact.last_name = data.last_name
        contact.email = data.email
        contact.phone = data.phone
        contact.birthday = data.birthday
        contact.additional_data = data.additional_data

        db.commit()
        db.refresh(contact)

    return contact


def get_upcoming_birthdays(db, user_id):
    """
    Get contacts with upcoming birthdays in the next 7 days.

    This function calculates which contacts have birthdays within the next 7 days,
    accounting for year changes (e.g., birthday in January for a contact with
    December birthday).

    Args:
        db (Session): Database session.
        user_id (int): Owner of contacts.

    Returns:
        list[Contact]: Contacts with upcoming birthdays.
    """
    today = date.today()
    next_week = today + timedelta(days=7)

    contacts = db.query(Contact).filter(
        Contact.user_id == user_id
    ).all()

    result = []

    for c in contacts:

        bd = datetime.strptime(
            c.birthday,
            "%Y-%m-%d"
        ).date()

        bd = bd.replace(year=today.year)

        if bd < today:
            bd = bd.replace(year=today.year + 1)

        if today <= bd <= next_week:
            result.append(c)

    return result


def delete_contact(db, contact_id, user_id):
    """
    Delete a contact by ID.

    Args:
        db (Session): Database session.
        contact_id (int): Contact ID.
        user_id (int): Owner of contact.

    Returns:
        Contact | None: Deleted contact or None if not found.
    """
    contact = db.query(Contact).filter(
        Contact.id == contact_id,
        Contact.user_id == user_id
    ).first()

    if contact:
        db.delete(contact)
        db.commit()

    return contact


def get_user_by_email(db, email: str):
    """
    Retrieve a user by email address.

    Args:
        db (Session): Database session.
        email (str): Email address to search for.

    Returns:
        User | None: User object if found, otherwise None.
    """
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db, user_id: int):
    """
    Retrieve a user by ID.

    Args:
        db (Session): Database session.
        user_id (int): User ID to search for.

    Returns:
        User | None: User object if found, otherwise None.
    """
    return db.query(User).filter(User.id == user_id).first()
