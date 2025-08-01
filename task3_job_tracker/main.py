from fastapi import FastAPI
from pydantic import BaseModel
from file_handler import load_applications, save_applications

app = FastAPI()



class JobApplication(BaseModel):
    name: str
    company: str
    position: str
    status: str



applications = load_applications()



@app.post("/applications/")
def add_application(app: JobApplication):
    try:
        applications.append(app.dict())
        save_applications(applications)
        return {"message": "Application added successfully", "application": app}
    except Exception as e:
        return {"error": str(e)}



@app.get("/applications/")
def get_all_applications():
    return applications



@app.get("/applications/search")
def search_applications(status: str):
    matched = [app for app in applications if app["status"].lower() == status.lower()]
    if matched:
        return matched
    return {"message": "No applications found with that status"}
