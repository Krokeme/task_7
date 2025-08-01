from fastapi import FastAPI, Query, Path
from pydantic import BaseModel, EmailStr
from typing import Optional

app = FastAPI()


contacts = {}


class Contact(BaseModel):
    phone: str
    email: EmailStr


@app.post("/contacts/")
def add_contact(name: str = Query(...), contact: Optional[Contact] = None):
    if not contact:
        return {"error": "Contact data is required."}
    if name in contacts:
        return {"error": f"Contact with name '{name}' already exists."}
    contacts[name] = contact.dict()
    return {"message": "Contact added successfully", "contact": contacts[name]}



@app.get("/contacts/")
def get_contact(name: str = Query(...)):
    if name not in contacts:
        return {"error": f"Contact with name '{name}' not found."}
    return {"name": name, "contact": contacts[name]}



@app.post("/contacts/{name}")
def update_contact(name: str = Path(...), contact: Optional[Contact] = None):
    if not contact:
        return {"error": "Updated contact data required."}
    if name not in contacts:
        return {"error": f"No contact found with name '{name}'."}
    contacts[name] = contact.dict()
    return {"message": "Contact updated successfully", "contact": contacts[name]}



@app.delete("/contacts/{name}")
def delete_contact(name: str = Path(...)):
    if name not in contacts:
        return {"error": f"No contact found with name '{name}'."}
    deleted = contacts.pop(name)
    return {"message": f"Contact '{name}' deleted successfully."}
