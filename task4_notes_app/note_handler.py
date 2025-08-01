import json
import os

FILE_NAME = "notes.json"

def load_notes():
    if not os.path.exists(FILE_NAME):
        return {}
    try:
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_notes(notes):
    with open(FILE_NAME, "w") as f:
        json.dump(notes, f, indent=4)

def add_note(title, content):
    notes = load_notes()
    if title in notes:
        return {"error": "Note already exists"}
    notes[title] = content
    save_notes(notes)
    return {"message": "Note added"}

def get_note(title):
    notes = load_notes()
    return {"content": notes.get(title)} if title in notes else {"error": "Note not found"}

def update_note(title, content):
    notes = load_notes()
    if title not in notes:
        return {"error": "Note not found"}
    notes[title] = content
    save_notes(notes)
    return {"message": "Note updated"}

def delete_note(title):
    notes = load_notes()
    if title not in notes:
        return {"error": "Note not found"}
    del notes[title]
    save_notes(notes)
    return {"message": "Note deleted"}
