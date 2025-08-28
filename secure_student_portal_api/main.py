from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import os, json

from auth import hash_password, safe_load_json, safe_save_json, get_current_student

app = FastAPI(title="Secure Student Portal API", version="1.0.0")

STUDENTS_FILE = "students.json"




class StudentRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=3)
    grades: List[int] = []

class StudentOut(BaseModel):
    username: str
    grades: List[int]




@app.post("/register/", status_code=status.HTTP_201_CREATED)
def register_student(payload: StudentRegister):
    students: Dict[str, Any] = safe_load_json(STUDENTS_FILE, default={})

    if payload.username in students:
        raise HTTPException(status_code=400, detail="Username already exists")

    students[payload.username] = {
        "password": hash_password(payload.password),
        "grades": payload.grades,
    }
    safe_save_json(STUDENTS_FILE, students)
    return {"message": f"Student {payload.username} registered successfully."}

@app.post("/login/")
def login_student(payload: StudentRegister):
    students: Dict[str, Any] = safe_load_json(STUDENTS_FILE, default={})
    student = students.get(payload.username)

    if not student or student["password"] != hash_password(payload.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": f"Welcome {payload.username}!", "grades": student["grades"]}

@app.get("/grades/", response_model=StudentOut)
def view_grades(student=Depends(get_current_student)):
    return {"username": student["username"], "grades": student["grades"]}

@app.get("/health")
def health():
    return {"status": "ok"}
