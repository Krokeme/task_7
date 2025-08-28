from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import json, os
from datetime import date

from auth import get_current_user

app = FastAPI(title="Job Application Tracker API", version="1.0.0")

APPLICATIONS_FILE = "applications.json"





class JobApplicationIn(BaseModel):
    job_title: str = Field(..., min_length=1, max_length=100)
    company: str = Field(..., min_length=1, max_length=100)
    date_applied: date
    status: str = Field(..., min_length=1, max_length=50)

class JobApplication(JobApplicationIn):
    username: str




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




@app.post("/applications/", response_model=JobApplication, status_code=status.HTTP_201_CREATED)
def add_application(payload: JobApplicationIn, user = Depends(get_current_user)):
    apps: Dict[str, List[Dict[str, Any]]] = safe_load_json(APPLICATIONS_FILE, default={})
    username = user["username"]

    new_app = {
        "username": username,
        "job_title": payload.job_title,
        "company": payload.company,
        "date_applied": str(payload.date_applied),
        "status": payload.status,
    }

    user_apps = apps.get(username, [])
    user_apps.append(new_app)
    apps[username] = user_apps
    safe_save_json(APPLICATIONS_FILE, apps)

    return new_app

@app.get("/applications/", response_model=List[JobApplication])
def list_applications(user = Depends(get_current_user)):
    apps: Dict[str, List[Dict[str, Any]]] = safe_load_json(APPLICATIONS_FILE, default={})
    return apps.get(user["username"], [])

@app.get("/health")
def health():
    return {"status": "ok"}
