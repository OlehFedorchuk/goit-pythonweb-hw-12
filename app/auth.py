from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
import os

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def verify_password(plain_password, hashed_password):
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password (str): The password provided by the user.
        hashed_password (str): The hashed password stored in the database.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def get_password_hash(password):
    """
    Hash a plain password using bcrypt algorithm.

    Args:
        password (str): Plain text password.

    Returns:
        str: Hashed password.
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create a JWT access token with expiration time.

    Adds an expiration claim ('exp') to the token payload and encodes it
    using the configured secret key and algorithm.

    Args:
        data (dict): Data to encode inside the token (e.g. user email).
        expires_delta (timedelta | None): Custom expiration time. Defaults to 15 minutes.

    Returns:
        str: Encoded JWT access token.
    """

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create a JWT refresh token with longer expiration time.

    Adds an expiration claim ('exp') to the token payload.
    Refresh tokens are long-lived and used to obtain new access tokens.

    Args:
        data (dict): Data to encode inside the token (e.g. user ID).
        expires_delta (timedelta | None): Custom expiration time. Defaults to 7 days.

    Returns:
        str: Encoded JWT refresh token.
    """

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt
