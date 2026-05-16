from uuid import uuid4
from unittest.mock import patch
from tests.conftest import client


@patch("app.routes.auth.send_verification_email")
def test_register_user(mock_send_email):
    unique_id = uuid4()
    response = client.post(
        "/auth/register",
        json={
            "email": f"{unique_id}@example.com",
            "username": f"user_{unique_id}",
            "password": "12345678"
        }
    )
    assert response.status_code == 201


def test_register_existing_user():
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "12345678"
        }
    )
    assert response.status_code == 409


def test_login_user():
    response = client.post(
        "/auth/login",
        data={
            "username": "test@example.com",
            "password": "12345678"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password():
    response = client.post(
        "/auth/login",
        data={
            "username": "test@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401

def test_login_returns_both_tokens():
    """Test that login returns both access_token and refresh_token."""
    response = client.post(
        "/auth/login",
        data={
            "username": "test@example.com",
            "password": "12345678"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_refresh_access_token():
    """Test refreshing access_token using refresh_token."""
    # First, login to get tokens
    login_response = client.post(
        "/auth/login",
        data={
            "username": "test@example.com",
            "password": "12345678"
        }
    )
    refresh_token = login_response.json()["refresh_token"]

    # Use refresh_token to get new access_token
    refresh_response = client.post(
        "/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    assert refresh_response.status_code == 200
    data = refresh_response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_refresh_with_invalid_token():
    """Test that invalid refresh_token is rejected."""
    response = client.post(
        "/auth/refresh",
        json={"refresh_token": "invalid_token_here"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or expired refresh token"


def test_logout():
    """Test logging out invalidates refresh_token."""
    # First, login to get tokens
    login_response = client.post(
        "/auth/login",
        data={
            "username": "test@example.com",
            "password": "12345678"
        }
    )
    refresh_token = login_response.json()["refresh_token"]

    # Logout using refresh_token
    logout_response = client.post(
        "/auth/logout",
        json={"refresh_token": refresh_token}
    )
    assert logout_response.status_code == 200
    assert logout_response.json()["message"] == "Logged out successfully"

    # Try to use the same refresh_token again - should fail
    refresh_response = client.post(
        "/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    assert refresh_response.status_code == 401


def test_logout_with_invalid_token():
    """Test logout with invalid token."""
    response = client.post(
        "/auth/logout",
        json={"refresh_token": "invalid_token"}
    )
    assert response.status_code == 401
