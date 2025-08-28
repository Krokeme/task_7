from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Dict

security = HTTPBasic()



USERS: Dict[str, Dict[str, str]] = {
    "alice": {"password": "alicepass", "role": "user"},
    "bob": {"password": "bobpass", "role": "user"},
    "admin": {"password": "adminpass", "role": "admin"},
}

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)) -> Dict[str, str]:
    username = credentials.username
    password = credentials.password

    user = USERS.get(username)
    if not user or user["password"] != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return {"username": username, "role": user["role"]}
