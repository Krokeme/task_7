from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlmodel import Session, select
from .database import get_session
from .models import User

security = HTTPBasic()

def get_current_user(
    credentials: HTTPBasicCredentials = Depends(security),
    session: Session = Depends(get_session),
):
    statement = select(User).where(User.username == credentials.username)
    user = session.exec(statement).first()
    if not user or user.password != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user
