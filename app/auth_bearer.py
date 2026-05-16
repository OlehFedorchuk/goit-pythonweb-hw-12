import os
import json
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models_user import User
from app.redis import redis_client

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

CACHE_TTL = 60 * 30  # 30 хв


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Get current authenticated user using JWT access_token + Redis cache + DB fallback.
    
    Validates the JWT token and retrieves the user from cache or database.
    """

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    cache_key = f"user:{email}"

    cached_user = redis_client.get(cache_key)

    if cached_user:
        user_data = json.loads(cached_user)
        return User(**user_data)


    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise credentials_exception


    redis_client.setex(
        cache_key,
        CACHE_TTL,
        json.dumps({
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "role": user.role
        })
    )

    return user


def get_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current user and verify they have admin role.
    
    Raises:
        HTTPException: 403 Forbidden if user is not an admin.
    
    Returns:
        User: The authenticated admin user.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only administrators can perform this action"
        )
    return current_user
