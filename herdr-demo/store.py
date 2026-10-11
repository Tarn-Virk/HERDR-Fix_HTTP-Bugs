"""Shared in-memory contact store. Every route imports from here.
Agents must NOT edit this file."""
from pydantic import BaseModel


class ContactIn(BaseModel):
    name: str
    email: str


# Seed data. Resets every time the server reloads.
contacts: list[dict] = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
    {"id": 4, "name": "Dana", "email": "dana@example.com"},
]

_next_id = 5


def next_id() -> int:
    global _next_id
    value = _next_id
    _next_id += 1
    return value


def find_contact(contact_id: int) -> dict | None:
    for contact in contacts:
        if contact["id"] == contact_id:
            return contact
    return None
