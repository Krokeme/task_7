from fastapi import FastAPI
from pydantic import BaseModel
import json
import os

app = FastAPI()



DATA_FILE = "students.json"



class Student(BaseModel):
    name: str
    subject_scores: dict



def load_students():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []



def save_students(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)



def calculate_grade(subject_scores):
    try:
        scores = list(subject_scores.values())
        avg = sum(scores) / len(scores)
        if avg >= 90:
            grade = "A"
        elif avg >= 80:
            grade = "B"
        elif avg >= 70:
            grade = "C"
        elif avg >= 60:
            grade = "D"
        else:
            grade = "F"
        return round(avg, 2), grade
    except:
        return 0.0, "F"



students = load_students()

# ===== Add student =====
@app.post("/students/")
def add_student(student: Student):
    for s in students:
        if s["name"].lower() == student.name.lower():
            return {"error": "Student already exists"}

    avg, grade = calculate_grade(student.subject_scores)
    student_data = student.dict()
    student_data["average"] = avg
    student_data["grade"] = grade

    students.append(student_data)
    save_students(students)

    return {"message": "Student added", "student": student_data}



@app.get("/students/")
def get_all_students():
    return students



@app.get("/students/{name}")
def get_student(name: str):
    for s in students:
        if s["name"].lower() == name.lower():
            return s
    return {"error": "Student not found"}
