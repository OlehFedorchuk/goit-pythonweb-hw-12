from unittest.mock import MagicMock, patch

from app.crud import (
    create_contact,
    get_contacts,
    get_contact_by_id,
    update_contact,
    delete_contact,
)


def test_get_contacts():
    db = MagicMock()

    query = db.query.return_value
    query.filter.return_value = query
    query.all.return_value = []

    result = get_contacts(db=db, user_id=1)

    assert result == []


def test_get_contact_by_id():
    db = MagicMock()

    mock_contact = MagicMock()
    mock_contact.id = 1
    mock_contact.first_name = "Oleh"

    query = db.query.return_value
    query.filter.return_value.first.return_value = mock_contact

    result = get_contact_by_id(
        db=db,
        contact_id=1,
        user_id=1
    )

    assert result.id == 1


@patch("app.crud.Contact")
def test_create_contact(mock_contact_class):
    db = MagicMock()

    body = MagicMock()
    body.model_dump.return_value = {
        "first_name": "Oleh",
        "last_name": "Test",
        "email": "test@test.com",
        "phone": "123456789",
        "birthday": "2000-01-01",
        "additional_data": "test"
    }

    mock_contact = MagicMock()
    mock_contact.first_name = "Oleh"

    mock_contact_class.return_value = mock_contact

    result = create_contact(
        db=db,
        contact=body,
        user_id=1
    )

    assert result.first_name == "Oleh"

    db.add.assert_called_once_with(mock_contact)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(mock_contact)

def test_update_contact():
    from tests.conftest import TestingSessionLocal
    from app.models import Contact
    from app.models_user import User
    from app.schemas import ContactCreate
    from datetime import date
    
    db = TestingSessionLocal()
    user = db.query(User).filter(User.email == "test@example.com").first()
    
    contact = Contact(
        first_name="OldName",
        last_name="OldLast",
        email="old@example.com",
        phone="+380501234567",
        birthday="1990-05-15",
        additional_data="Old",
        user_id=user.id
    )
    db.add(contact)
    db.commit()
    contact_id = contact.id
    
    update_data = ContactCreate(
        first_name="NewName",
        last_name="NewLast",
        email="new@example.com",
        phone="+380501234567",
        birthday=date(1990, 5, 15),
        additional_data="New"
    )
    
    result = update_contact(
        db=db,
        contact_id=contact_id,
        data=update_data,
        user_id=user.id
    )

    assert result is not None
    assert result.first_name == "NewName"
    db.delete(result)
    db.commit()
    db.close()


def test_delete_contact():
    db = MagicMock()

    mock_contact = MagicMock()

    query = db.query.return_value
    query.filter.return_value.first.return_value = mock_contact

    result = delete_contact(
        db=db,
        contact_id=1,
        user_id=1
    )

    assert result == mock_contact