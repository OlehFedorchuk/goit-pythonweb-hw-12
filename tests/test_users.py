"""Original user tests."""

from tests.conftest import client, get_token
from unittest.mock import patch, MagicMock
import pytest


@pytest.fixture
def user_headers():
    """Get user headers."""
    token = get_token()
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers():
    """Get admin headers."""
    token = get_token(email="admin@example.com")
    return {"Authorization": f"Bearer {token}"}


def test_get_me(user_headers):
    response = client.get(
        "/users/me",
        headers=user_headers
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
    assert response.json()["role"] == "user"


def test_get_me_admin(admin_headers):
    response = client.get(
        "/users/me",
        headers=admin_headers
    )
    assert response.status_code == 200
    assert response.json()["email"] == "admin@example.com"
    assert response.json()["role"] == "admin"


@patch("app.routes.users.cloudinary.uploader.upload")
def test_avatar_upload_admin_success(mock_upload, admin_headers):
    """Test that admin can upload avatar"""
    import io
    
    mock_upload.return_value = {"secure_url": "https://res.cloudinary.com/test/image.jpg"}
    
    file = io.BytesIO(b"fake image content")
    response = client.patch(
        "/users/avatar",
        headers=admin_headers,
        files={"file": ("test.jpg", file, "image/jpeg")}
    )
    assert response.status_code == 200
    assert "avatar" in response.json()
    assert response.json()["avatar"] == "https://res.cloudinary.com/test/image.jpg"


def test_avatar_upload_user_forbidden(user_headers):
    """Test that regular user cannot upload avatar"""
    import io
    
    file = io.BytesIO(b"fake image content")
    response = client.patch(
        "/users/avatar",
        headers=user_headers,
        files={"file": ("test.jpg", file, "image/jpeg")}
    )
    assert response.status_code == 403
    assert "administrator" in response.json()["detail"].lower()


def test_avatar_upload_unauthorized():
    """Test that unauthenticated user cannot upload avatar"""
    import io
    
    file = io.BytesIO(b"fake image content")
    response = client.patch(
        "/users/avatar",
        files={"file": ("test.jpg", file, "image/jpeg")}
    )
    # Unauthenticated access to protected endpoint returns 403 (not 401)
    # because OAuth2PasswordBearer raises HTTPException with 403
    assert response.status_code in [401, 403]
