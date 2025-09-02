import json
from models import Note
from sqlmodel import Session, select

def backup_notes(session: Session):
    notes = session.exec(select(Note)).all()
    data = [
        {"id": n.id, "title": n.title, "content": n.content, "created_at": str(n.created_at)}
        for n in notes
    ]
    with open("notes.json", "w") as f:
        json.dump(data, f, indent=4)
