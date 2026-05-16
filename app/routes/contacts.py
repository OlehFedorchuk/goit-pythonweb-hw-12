from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Contact
from app.models_user import User

from app.schemas import ContactSchema, ContactCreate, ContactResponse
from app.auth_bearer import get_current_user
import app.crud as crud

router = APIRouter(
    prefix="/contacts",
    tags=["contacts"]
)


@router.post("/", status_code=201)
def create_contact(
    body: ContactSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new contact for the authenticated user.

    Args:
        body (ContactSchema): Data required to create a contact.
        db (Session): Database session dependency.
        current_user (User): Currently authenticated user.

    Returns:
        Contact: The created contact object.
    """

    contact = Contact(
        **body.model_dump(),
        user_id=current_user.id
    )

    db.add(contact)
    db.commit()
    db.refresh(contact)

    return contact


@router.get("/")
def get_contacts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve all contacts for the authenticated user.

    Args:
        db (Session): Database session dependency.
        current_user (User): Currently authenticated user.

    Returns:
        list[Contact]: List of user contacts.
    """

    contacts = db.query(Contact).filter(
        Contact.user_id == current_user.id
    ).all()

    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve a specific contact by ID.

    Args:
        contact_id (int): ID of the contact.
        db (Session): Database session dependency.
        current_user (User): Currently authenticated user.

    Raises:
        HTTPException: 404 if contact is not found.

    Returns:
        ContactResponse: The requested contact.
    """

    contact = crud.get_contact_by_id(db, contact_id, current_user.id)

    if contact is None:
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )

    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact(
    contact_id: int,
    contact_data: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing contact.

    Args:
        contact_id (int): ID of the contact to update.
        contact_data (ContactCreate): Updated contact data.
        db (Session): Database session dependency.
        current_user (User): Currently authenticated user.

    Raises:
        HTTPException: 404 if contact is not found.

    Returns:
        ContactResponse: Updated contact object.
    """

    contact = crud.update_contact(
        db,
        contact_id,
        contact_data,
        current_user.id
    )

    if contact is None:
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )

    return contact


@router.get("/birthdays/upcoming", response_model=list[ContactResponse])
def upcoming_birthdays(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve contacts with upcoming birthdays.

    Args:
        db (Session): Database session dependency.
        current_user (User): Currently authenticated user.

    Returns:
        list[ContactResponse]: Contacts with upcoming birthdays.
    """

    return crud.get_upcoming_birthdays(
        db,
        current_user.id
    )


@router.delete("/{contact_id}")
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a contact by ID.

    Args:
        contact_id (int): ID of the contact to delete.
        db (Session): Database session dependency.
        current_user (User): Currently authenticated user.

    Raises:
        HTTPException: 404 if contact is not found.

    Returns:
        dict: Confirmation message.
    """

    contact = crud.delete_contact(
        db,
        contact_id,
        current_user.id
    )

    if contact is None:
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )

    return {"message": "Contact deleted successfully"}