from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..core.security import create_access_token, verify_password
from ..models import User


def login(db: Session, email: str, password: str) -> dict:
    user = db.query(User).filter(User.email == email).one_or_none()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(subject=user.id, role=user.role.value, email=user.email)
    return {
        "token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "fullName": user.full_name,
            "role": user.role.value,
        },
    }
