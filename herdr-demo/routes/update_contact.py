"""PUT /contacts/{contact_id} - edit a contact. Owned by Agent 3."""
from fastapi import APIRouter, HTTPException

from store import ContactIn, find_contact

router = APIRouter()


@router.put("/contacts/{contact_id}")
def update_contact(contact_id: int, body: ContactIn):
    contact = find_contact(contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    updated = {**contact, "name": body.name, "email": body.email}
    return updated
