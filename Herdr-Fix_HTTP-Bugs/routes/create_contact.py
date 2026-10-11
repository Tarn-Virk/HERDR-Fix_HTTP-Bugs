"""POST /contacts - add a contact. Owned by Agent 2."""
from fastapi import APIRouter

from store import ContactIn, contacts, next_id

router = APIRouter()


@router.post("/contacts", status_code=201)
def create_contact(body: ContactIn):
    contact = {"id": next_id(), "name": body.name, "email": body.email}
    contacts.append(contact)
    return contact
