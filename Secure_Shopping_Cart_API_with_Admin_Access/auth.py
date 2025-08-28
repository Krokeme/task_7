from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Dict

security = HTTPBasic()



USERS: Dict[str, Dict[str, str]] = {
    "admin": {"password": "adminpass", "role": "admin"},
    "alice": {"password": "alicepass", "role": "customer"},
    "bob": {"password": "bobpass", "role": "customer"},
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

def require_role(role: str):
    def role_dependency(user: Dict[str, str] = Depends(get_current_user)) -> Dict[str, str]:
        if user["role"] != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions: requires role '{role}'",
            )
        return user
    return role_dependency
