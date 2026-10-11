"""GET /contacts - list every contact. Owned by Agent 1."""
from fastapi import APIRouter

from store import contacts

router = APIRouter()


@router.get("/contacts")
def get_contacts():
    return contacts
