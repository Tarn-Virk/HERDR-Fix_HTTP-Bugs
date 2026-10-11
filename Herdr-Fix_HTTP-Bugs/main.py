"""App entry point. Wires the four route files together and serves the page.
Agents must NOT edit this file."""
from fastapi import FastAPI
from fastapi.responses import FileResponse

from routes import create_contact, delete_contact, get_contacts, update_contact

app = FastAPI(title="Herdr Demo - Contacts API")

app.include_router(get_contacts.router)
app.include_router(create_contact.router)
app.include_router(update_contact.router)
app.include_router(delete_contact.router)


@app.get("/")
def home():
    return FileResponse("static/index.html")
