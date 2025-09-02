from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List
from datetime import date
from ..database import get_session
from ..models import JobApplication, User
from ..auth import get_current_user

router = APIRouter(prefix="/applications", tags=["Applications"])

@router.post("/", response_model=JobApplication)
def add_application(
    application: JobApplication,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    application.user_id = user.id
    application.date_applied = application.date_applied or date.today()
    session.add(application)
    session.commit()
    session.refresh(application)
    return application

@router.get("/", response_model=List[JobApplication])
def list_applications(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    statement = select(JobApplication).where(JobApplication.user_id == user.id)
    return session.exec(statement).all()

@router.get("/search", response_model=List[JobApplication])
def search_applications(
    status: str = Query(..., description="Filter by status (e.g., pending, accepted)"),
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    try:
        statement = (
            select(JobApplication)
            .where(JobApplication.user_id == user.id, JobApplication.status == status)
        )
        return session.exec(statement).all()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid query")
