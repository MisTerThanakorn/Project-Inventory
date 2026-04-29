from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.deps import get_current_user
from backend.app.schemas import ApiResponse, LoginRequest, UserRead
from backend.app.services.auth_service import login as login_service

router = APIRouter()


@router.post("/login", response_model=ApiResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return {"success": True, "data": login_service(db, payload.email, payload.password)}


@router.get("/me", response_model=ApiResponse)
def me(current_user=Depends(get_current_user)):
    user = UserRead.model_validate(current_user).model_dump(by_alias=True)
    return {"success": True, "data": user}
