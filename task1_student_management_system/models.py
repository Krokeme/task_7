from sqlmodel import SQLModel, Field
from typing import Optional, List
from pydantic import EmailStr

class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    email: EmailStr
    grades: str 
