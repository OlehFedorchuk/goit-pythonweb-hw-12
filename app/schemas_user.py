"""
User Pydantic schemas.

This module defines request and response schemas for User-related operations.
These schemas are used for data validation and serialization in FastAPI.

Schemas:
    UserCreate: Used for user registration.
    UserResponse: Used for returning user data in API responses.
    TokenResponse: Used for returning JWT tokens in authentication endpoints.
    RefreshTokenRequest: Used for refresh token endpoint.
"""

from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict

class UserCreate(BaseModel):
    """
    Schema for creating a new user.

    Used during registration to validate incoming user data.

    Attributes:
        email (EmailStr): Valid user email address.
        username (str): Unique username.
        password (str): Plain text password (will be hashed before storage).
    """

    email: EmailStr
    username: str
    password: str


class UserResponse(BaseModel):
    """
    Schema for returning user data in API responses.

    Used to expose safe user information to clients.

    Attributes:
        id (int): User ID.
        email (EmailStr): User email address.
        username (str): Username.
        avatar (str | None): URL to user avatar image.
        role (str): User role ('user' or 'admin').
    """

    id: int
    email: EmailStr
    username: str
    avatar: str | None = None
    role: str = "user"

    class Config:
        """
        Pydantic configuration.

        Enables ORM mode (from_attributes) so SQLAlchemy models
        can be converted directly into Pydantic schemas.
        """
        model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    """
    Schema for returning JWT tokens in authentication endpoints.

    Used in login and refresh endpoints to return both access and refresh tokens.

    Attributes:
        access_token (str): Short-lived JWT token for API access (15 minutes).
        refresh_token (str): Long-lived JWT token for obtaining new access tokens (7 days).
        token_type (str): Token type, always "bearer".
    """

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    """
    Schema for refresh token endpoint request.

    Used to exchange a refresh token for a new access token.

    Attributes:
        refresh_token (str): The refresh token obtained from login.
    """

    refresh_token: str
