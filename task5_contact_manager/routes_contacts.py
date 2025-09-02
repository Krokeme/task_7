from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models import Contact
from auth import get_current_user, User

router = APIRouter()

@router.post("/")
def create_contact(contact: Contact, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    contact.user_id = user.id
    session.add(contact)
    session.commit()
    session.refresh(contact)
    return contact

@router.get("/")
def list_contacts(session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    contacts = session.exec(select(Contact).where(Contact.user_id == user.id)).all()
    return contacts

@router.put("/{contact_id}")
def update_contact(contact_id: int, updated: Contact, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    contact = session.get(Contact, contact_id)
    if not contact or contact.user_id != user.id:
        raise HTTPException(status_code=404, detail="Contact not found")
    contact.name = updated.name
    contact.email = updated.email
    contact.phone = updated.phone
    session.add(contact)
    session.commit()
    session.refresh(contact)
    return contact

@router.delete("/{contact_id}")
def delete_contact(contact_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    contact = session.get(Contact, contact_id)
    if not contact or contact.user_id != user.id:
        raise HTTPException(status_code=404, detail="Contact not found")
    session.delete(contact)
    session.commit()
    return {"msg": "Contact deleted"}
