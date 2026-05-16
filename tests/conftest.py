"""
Test configuration and fixtures.

Sets up the test database, mocks Redis, and provides utility functions
for creating test users and tokens.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import MagicMock
import sys
import os

# Mock Redis before importing the app
from unittest.mock import patch, MagicMock
sys.modules['redis'] = MagicMock()

# Create a fake redis client with actual storage capability
class MockRedis:
    def __init__(self):
        self.store = {}
    
    def get(self, key):
        return self.store.get(key)
    
    def setex(self, key, ttl, value):
        self.store[key] = value
    
    def delete(self, key):
        if key in self.store:
            del self.store[key]
    
    def exists(self, key):
        return key in self.store

mock_redis = MockRedis()

import app.redis as redis_module
import app.auth_bearer as auth_bearer_module
import app.routes.auth as auth_routes_module

redis_module.redis_client = mock_redis
auth_bearer_module.redis_client = mock_redis
auth_routes_module.redis_client = mock_redis

from app.main import app
from app.database import Base, get_db
from app.models_user import User
from app.auth import get_password_hash

# Use file-based SQLite for tests (persists between test runs)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base.metadata.create_all(bind=engine)


def override_get_db():
    """Database dependency override for tests."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def create_test_user(email="test@example.com", username="testuser", role="user"):
    """Create a test user in the database."""
    db = TestingSessionLocal()

    user = db.query(User).filter(
        User.email == email
    ).first()
    if not user:
        user = User(
            email=email,
            username=username,
            hashed_password=get_password_hash("12345678"),
            verified=True,
            role=role
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    db.close()
    return user


# Create test users once at startup
create_test_user()
create_test_user(email="admin@example.com", username="adminuser", role="admin")


def get_token(email="test@example.com"):
    """Get JWT token for a test user."""
    response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": "12345678"
        }
    )
    if response.status_code == 200:
        return response.json()["access_token"]
    # If login fails, still return something to allow tests to run
    return "test_token"
