from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import date

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str  # in production, store hashed password
    applications: List["JobApplication"] = Relationship(back_populates="owner")

class JobApplication(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company: str
    position: str
    status: str
    date_applied: date

    user_id: int = Field(foreign_key="user.id")
    owner: Optional[User] = Relationship(back_populates="applications")
