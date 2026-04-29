from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.deps import get_current_user
from backend.app.schemas import ApiResponse, ItemCreate, ItemRead, ItemUpdate
from backend.app.services import item_service

router = APIRouter()


@router.get("", response_model=ApiResponse)
def list_records(
    search: str | None = Query(default=None),
    status_filter: str | None = Query(default=None, alias="status"),
    category_id: str | None = Query(default=None, alias="categoryId"),
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),
):
    items = item_service.list_items(db, search=search, status_filter=status_filter, category_id=category_id)
    return {"success": True, "data": [ItemRead.model_validate(item).model_dump(by_alias=True) for item in items]}


@router.get("/summary", response_model=ApiResponse)
def get_summary(db: Session = Depends(get_db), _current_user=Depends(get_current_user)):
    return {"success": True, "data": item_service.summary(db)}


@router.get("/{item_id}", response_model=ApiResponse)
def get_record(item_id: str, db: Session = Depends(get_db), _current_user=Depends(get_current_user)):
    item = item_service.get_item(db, item_id)
    return {"success": True, "data": ItemRead.model_validate(item).model_dump(by_alias=True)}


@router.post("", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
def create_record(
    payload: ItemCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    item = item_service.create_item(db, payload.model_dump(), current_user.id)
    return {"success": True, "data": ItemRead.model_validate(item).model_dump(by_alias=True)}


@router.patch("/{item_id}", response_model=ApiResponse)
def update_record(item_id: str, payload: ItemUpdate, db: Session = Depends(get_db), _current_user=Depends(get_current_user)):
    item = item_service.update_item(db, item_id, payload.model_dump(exclude_unset=True))
    return {"success": True, "data": ItemRead.model_validate(item).model_dump(by_alias=True)}


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_record(item_id: str, db: Session = Depends(get_db), _current_user=Depends(get_current_user)):
    item_service.delete_item(db, item_id)
    return None
