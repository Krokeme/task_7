from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import Note
from database import get_session
from utils.backup import backup_notes

router = APIRouter(prefix="/notes", tags=["Notes"])

@router.post("/")
def create_note(note: Note, session: Session = Depends(get_session)):
    session.add(note)
    session.commit()
    session.refresh(note)
    backup_notes(session)
    return note

@router.get("/")
def list_notes(session: Session = Depends(get_session)):
    notes = session.exec(select(Note)).all()
    return notes

@router.get("/{note_id}")
def get_note(note_id: int, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.delete("/{note_id}")
def delete_note(note_id: int, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    session.delete(note)
    session.commit()
    backup_notes(session)
    return {"message": "Note deleted"}
