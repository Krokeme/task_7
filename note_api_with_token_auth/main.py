from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import json, os
from datetime import datetime

from auth import authenticate_user, create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI(title="Notes API with JWT Auth (PyJWT)", version="1.0.0")

NOTES_FILE = "notes.json"




class NoteIn(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)

class Note(NoteIn):
    date: str
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str




def safe_load_json(path: str, default):
    try:
        if not os.path.exists(path):
            return default
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return default

def safe_save_json(path: str, data: Any):
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)
    os.replace(tmp_path, path)




@app.post("/login/", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = authenticate_user(form_data.username, form_data.password)
    if not username:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token({"sub": username})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/notes/", response_model=Note, status_code=status.HTTP_201_CREATED)
def add_note(payload: NoteIn, username: str = Depends(get_current_user)):
    notes: Dict[str, List[Dict[str, Any]]] = safe_load_json(NOTES_FILE, default={})

    new_note = {
        "username": username,
        "title": payload.title,
        "content": payload.content,
        "date": datetime.utcnow().isoformat()
    }

    user_notes = notes.get(username, [])
    user_notes.append(new_note)
    notes[username] = user_notes
    safe_save_json(NOTES_FILE, notes)

    return new_note

@app.get("/notes/", response_model=List[Note])
def list_notes(username: str = Depends(get_current_user)):
    notes: Dict[str, List[Dict[str, Any]]] = safe_load_json(NOTES_FILE, default={})
    return notes.get(username, [])

@app.get("/health")
def health():
    return {"status": "ok"}
