"""
Contact Pydantic schemas.

This module defines request and response schemas for Contact operations.
These schemas are used for validation, serialization, and API contracts
in the FastAPI application.

Schemas:
    ContactSchema: Base schema for contact data.
    ContactCreate: Schema used when creating a contact.
    ContactResponse: Schema used when returning contact data.
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from pydantic import ConfigDict

class ContactSchema(BaseModel):
    """
    Base schema for contact data.

    This schema defines the common fields used for creating and
    validating contact information.

    Attributes:
        first_name (str): First name of the contact.
        last_name (str): Last name of the contact.
        email (str): Email address of the contact.
        phone (str): Phone number.
        birthday (str): Birthday date in string format.
        additional_data (str): Extra information about the contact.
    """
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_length=2)
    email: str
    phone: str = Field(min_length=10)
    birthday: date
    additional_data: str


class ContactCreate(ContactSchema):
    """
    Schema for creating a new contact.

    Inherits all fields from ContactSchema.
    Used for POST /contacts endpoint.
    """
    pass


class ContactResponse(ContactSchema):
    """
    Schema for returning contact data in API responses.

    Includes database-generated fields such as ID.

    Attributes:
        id (int): Unique identifier of the contact.
    """

    id: int

    class Config:
        """
        Pydantic configuration.

        Enables ORM mode so SQLAlchemy models can be
        converted directly into Pydantic schemas.
        """
        model_config = ConfigDict(from_attributes=True)

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str