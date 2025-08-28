import hashlib
import json, os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Dict, Any

security = HTTPBasic()
STUDENTS_FILE = "students.json"

def hash_password(password: str) -> str:
   
    return hashlib.sha256(password.encode()).hexdigest()

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
        json.dump(data, f, indent=2)
    os.replace(tmp_path, path)

def get_current_student(credentials: HTTPBasicCredentials = Depends(security)) -> Dict[str, Any]:
    students = safe_load_json(STUDENTS_FILE, {})
    username = credentials.username
    password = credentials.password
    student = students.get(username)

    if not student or student["password"] != hash_password(password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return {"username": username, "grades": student["grades"]}
