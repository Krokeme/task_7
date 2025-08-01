from fastapi import FastAPI, Query
from pydantic import BaseModel
from note_handler import add_note, get_note, update_note, delete_note

app = FastAPI()

class Note(BaseModel):
    content: str

# http://127.0.0.1:8000/notes/?title=meetup
# "meeting" is

# http://127.0.0.1:8000/notes/meetup/


@app.post("/notes/")
def create_note(title: str = Query(...), note: Note = None):
    return add_note(title, note.content)

@app.get("/notes/{title}")
def read_note(title: str):
    return get_note(title)

@app.post("/notes/{title}")
def edit_note(title: str, note: Note = None):
    return update_note(title, note.content)

@app.delete("/notes/{title}")
def remove_note(title: str):
    return delete_note(title)
