"""Original contacts integration tests."""

from tests.conftest import client, get_token, TestingSessionLocal
from app.models import Contact
from app.models_user import User
import pytest


@pytest.fixture
def user_headers():
    """Get user headers."""
    token = get_token()
    return {"Authorization": f"Bearer {token}"}


def test_create_contact(user_headers):
    response = client.post(
        "/contacts/",
        headers=user_headers,
        json={
            "first_name": "Test",
            "last_name": "Contact",
            "email": "contact@example.com",
            "phone": "+380501234567",
            "birthday": "1990-05-15",
            "additional_data": "Test"
        }
    )
    assert response.status_code == 201


def test_get_contacts(user_headers):
    response = client.get(
        "/contacts/",
        headers=user_headers
    )
    assert response.status_code == 200


def test_get_contact_by_id(user_headers):
    db = TestingSessionLocal()
    user = db.query(User).filter(User.email == "test@example.com").first()
    
    contact = Contact(
        first_name="GetTest",
        last_name="Contact",
        email="gettest@example.com",
        phone="+380501234567",
        birthday="1990-05-15",
        additional_data="Test",
        user_id=user.id
    )
    db.add(contact)
    db.commit()
    contact_id = contact.id
    db.close()
    
    response = client.get(
        f"/contacts/{contact_id}",
        headers=user_headers
    )
    assert response.status_code == 200


def test_update_contact(user_headers):
    db = TestingSessionLocal()
    user = db.query(User).filter(User.email == "test@example.com").first()
    
    contact = Contact(
        first_name="UpdateTest",
        last_name="Contact",
        email="updatetest@example.com",
        phone="+380501234567",
        birthday="1990-05-15",
        additional_data="Test",
        user_id=user.id
    )
    db.add(contact)
    db.commit()
    contact_id = contact.id
    db.close()
    
    response = client.put(
        f"/contacts/{contact_id}",
        headers=user_headers,
        json={
            "first_name": "Updated",
            "last_name": "Contact",
            "email": "updated@example.com",
            "phone": "+380501234567",
            "birthday": "1990-05-15",
            "additional_data": "Updated"
        }
    )
    assert response.status_code == 200


def test_delete_contact(user_headers):
    db = TestingSessionLocal()
    user = db.query(User).filter(User.email == "test@example.com").first()
    
    contact = Contact(
        first_name="DeleteTest",
        last_name="Contact",
        email="deletetest@example.com",
        phone="+380501234567",
        birthday="1990-05-15",
        additional_data="Test",
        user_id=user.id
    )
    db.add(contact)
    db.commit()
    contact_id = contact.id
    db.close()
    
    response = client.delete(
        f"/contacts/{contact_id}",
        headers=user_headers
    )
    assert response.status_code == 200
