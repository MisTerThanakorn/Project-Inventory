from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.deps import get_current_user
from backend.app.schemas import ApiResponse
from backend.app.services.item_service import summary

router = APIRouter()


@router.get("/summary", response_model=ApiResponse)
def get_dashboard_summary(db: Session = Depends(get_db), _current_user=Depends(get_current_user)):
    return {"success": True, "data": summary(db)}
