from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
import os
from app.database import get_db
from app.models_user import User
from app.schemas import ResetPasswordRequest
from app.schemas_user import UserCreate, TokenResponse, RefreshTokenRequest
import uuid
from app.redis import redis_client
from app import crud
from app.email_service import send_reset_email
from app.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token
)
from app.email_service import (
    send_verification_email,
    create_email_token,
    confirm_email_token
)

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]

REFRESH_TOKEN_TTL = 60 * 60 * 24 * 8


@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    key = f"reset:{data.token}"
    user_id = redis_client.get(key)
    if user_id is None:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user = crud.get_user_by_id(db, int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.hashed_password = get_password_hash(data.new_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    redis_client.delete(key)
    
    redis_client.delete(f"refresh_tokens:{user.id}")
    
    return {"message": "Password successfully updated"}


@router.post("/request-password-reset")
def request_password_reset(email: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email)
    response = {"message": "If email exists, reset link will be sent"}

    if not user:
        return response
    token = str(uuid.uuid4())
    redis_client.setex(
        f"reset:{token}",
        900,
        str(user.id)
    )

    send_reset_email(email, token)
    return response


@router.post("/register", status_code=201)
async def register(
    body: UserCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Register a new user account.

    This endpoint:
    - Checks if a user with the same email or username already exists
    - Hashes the password securely
    - Creates a new user in the database
    - Generates an email verification token
    - Sends a verification email in the background

    Args:
        body (UserCreate): User registration data (email, username, password).
        background_tasks (BackgroundTasks): FastAPI background task manager.
        request (Request): HTTP request object (used to get base URL).
        db (Session): Database session dependency.

    Raises:
        HTTPException:
            - 409 if email or username already exists
            - 409 if database integrity constraint is violated

    Returns:
        dict: Success message indicating that verification email was sent.
    """

    existing_user = db.query(User).filter(
        (User.email == body.email) |
        (User.username == body.username)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email or username already exists"
        )

    hashed_password = get_password_hash(body.password)

    new_user = User(
        email=body.email,
        username=body.username,
        hashed_password=hashed_password,
        verified=False
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email or username already exists"
        )

    token = create_email_token(new_user.email)

    background_tasks.add_task(
        send_verification_email,
        new_user.email,
        str(request.base_url),
        token
    )

    return {
        "message": "User created successfully. Please check your email to verify your account."
    }


@router.get("/verify")
async def verify_email(
    token: str,
    db: Session = Depends(get_db)
):
    """
    Verify a user's email address using a token.

    This endpoint:
    - Decodes and validates the email verification token
    - Finds the corresponding user
    - Marks the user as verified if not already verified

    Args:
        token (str): Email verification token.
        db (Session): Database session dependency.

    Raises:
        HTTPException:
            - 400 if token is invalid or expired
            - 400 if user is not found

    Returns:
        dict: Message confirming verification status.
    """

    try:
        email = confirm_email_token(token)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired token"
        )

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="User not found"
        )

    if user.verified:
        return {"message": "Email already verified"}

    user.verified = True
    db.commit()

    return {"message": "Email verified successfully"}


@router.post("/login", response_model=TokenResponse)
def login(
    body: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return JWT tokens (access + refresh).

    This endpoint:
    - Validates user credentials
    - Checks if the account is verified
    - Generates both access_token (15 min) and refresh_token (7 days)
    - Stores refresh_token in Redis for validation and revocation

    Args:
        body (OAuth2PasswordRequestForm): Login form data (username=email, password).
        db (Session): Database session dependency.

    Raises:
        HTTPException:
            - 401 if credentials are invalid
            - 403 if email is not verified

    Returns:
        TokenResponse: Contains access_token, refresh_token, and token_type.
    """

    user = db.query(User).filter(
        User.email == body.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(body.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not user.verified:
        raise HTTPException(
            status_code=403,
            detail="Email not verified"
        )

    
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    
    redis_client.setex(
        f"refresh_tokens:{user.id}",
        REFRESH_TOKEN_TTL,
        refresh_token
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=TokenResponse)
def refresh_access_token(
    body: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Exchange refresh_token for a new access_token.

    This endpoint:
    - Validates the refresh_token JWT
    - Checks if token exists and is valid in Redis
    - Issues a new short-lived access_token
    - Optionally rotates the refresh_token for enhanced security

    Args:
        body (RefreshTokenRequest): Request containing refresh_token.
        db (Session): Database session dependency.

    Raises:
        HTTPException:
            - 401 if refresh_token is invalid or expired
            - 401 if refresh_token is not found in Redis (revoked)
            - 404 if user is not found

    Returns:
        TokenResponse: New access_token, refresh_token (rotated), and token_type.
    """

    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid or expired refresh token"
    )

    
    try:
        payload = jwt.decode(
            body.refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        
        user_id = int(user_id)

    except (JWTError, ValueError):
        raise credentials_exception


    stored_token = redis_client.get(f"refresh_tokens:{user_id}")

    if not stored_token:
        raise credentials_exception

    
    if stored_token != body.refresh_token:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    access_token = create_access_token(data={"sub": user.email})

    new_refresh_token = create_refresh_token(data={"sub": str(user.id)})

    redis_client.setex(
        f"refresh_tokens:{user.id}",
        REFRESH_TOKEN_TTL,
        new_refresh_token
    )

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


@router.post("/logout")
def logout(
    body: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Logout user by invalidating their refresh_token.

    This endpoint:
    - Validates the refresh_token
    - Removes the token from Redis, preventing further token refreshes
    - This forces the user to login again when access_token expires

    Args:
        body (RefreshTokenRequest): Request containing refresh_token.
        db (Session): Database session dependency.

    Raises:
        HTTPException:
            - 401 if refresh_token is invalid

    Returns:
        dict: Confirmation message.
    """

    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid refresh token"
    )

    try:
        payload = jwt.decode(
            body.refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user_id = int(user_id)

    except (JWTError, ValueError):
        raise credentials_exception

    redis_client.delete(f"refresh_tokens:{user_id}")

    return {"message": "Logged out successfully"}
