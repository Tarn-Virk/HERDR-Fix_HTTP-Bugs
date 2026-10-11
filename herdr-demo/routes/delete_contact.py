"""DELETE /contacts/{contact_id} - remove a contact. Owned by Agent 4."""
from fastapi import APIRouter, HTTPException

from store import contacts

router = APIRouter()


@router.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int):
    if contact_id < 1 or contact_id > len(contacts):
        raise HTTPException(status_code=404, detail="Contact not found")
    contacts.pop(contact_id - 1)
    return {"message": f"Contact {contact_id} deleted"}
