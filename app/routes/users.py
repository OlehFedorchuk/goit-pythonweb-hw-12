from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

import cloudinary.uploader
import app.cloudinary_service

from app.database import get_db
from app.models_user import User
from app.auth_bearer import get_current_user, get_admin_user

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

limiter = Limiter(
    key_func=get_remote_address
)


@router.get("/me")
@limiter.limit("5/minute")
def me(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """
    Get the currently authenticated user's profile.

    This endpoint returns the user data for the authenticated user.
    It is rate-limited to 5 requests per minute per IP address.

    Args:
        request (Request): Incoming HTTP request (used for rate limiting).
        current_user (User): Currently authenticated user.

    Returns:
        User: The authenticated user's data.
    """
    return current_user

@router.patch("/avatar")

async def update_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
    

):
    """
    Update the admin user's avatar image.

    Only users with admin role can upload/change their avatar.
    Uploads the image to Cloudinary and updates the user's avatar URL
    in the database.

    Args:
        file (UploadFile): Image file uploaded by the user.
        db (Session): Database session dependency.
        admin_user (User): Currently authenticated admin user.

    Returns:
        dict: Updated avatar URL.
    
    Raises:
        HTTPException: 403 Forbidden if user is not an admin.
    """
    result = cloudinary.uploader.upload(
        file.file,
        public_id=admin_user.username,
        overwrite=True
    )

    user = db.query(User).filter(User.id == admin_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.avatar = result["secure_url"]
    db.commit()
    db.refresh(user)
    return {
        "avatar": user.avatar
    }