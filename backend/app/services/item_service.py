from decimal import Decimal
from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from ..models import Category, Item, ItemStatus


def _apply_item_payload(item: Item, payload: dict) -> Item:
    for key, value in payload.items():
        if value is not None:
            setattr(item, key, value)
    if "category_id" in payload and payload["category_id"] is None:
        item.category_id = None
    return item


def list_items(db: Session, search: str | None = None, status_filter: str | None = None, category_id: str | None = None) -> list[Item]:
    query = db.query(Item).options(joinedload(Item.category), joinedload(Item.created_by))

    if search:
        pattern = f"%{search}%"
        query = query.filter((Item.sku.ilike(pattern)) | (Item.name.ilike(pattern)))
    if status_filter:
        query = query.filter(Item.status == ItemStatus(status_filter))
    if category_id:
        query = query.filter(Item.category_id == category_id)

    return query.order_by(Item.updated_at.desc()).all()


def get_item(db: Session, item_id: str) -> Item:
    item = (
        db.query(Item)
        .options(joinedload(Item.category), joinedload(Item.created_by))
        .filter(Item.id == item_id)
        .one_or_none()
    )
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


def create_item(db: Session, payload: dict, created_by_id: str | None) -> Item:
    item = Item(
        id=uuid4().hex,
        sku=payload["sku"],
        name=payload["name"],
        description=payload.get("description"),
        quantity=payload.get("quantity", 0),
        min_quantity=payload.get("min_quantity", 0),
        location=payload.get("location"),
        price=Decimal(str(payload.get("price", 0))),
        status=ItemStatus(payload.get("status", "ACTIVE")),
        category_id=payload.get("category_id"),
        created_by_id=created_by_id,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return get_item(db, item.id)


def update_item(db: Session, item_id: str, payload: dict) -> Item:
    item = get_item(db, item_id)
    if "sku" in payload and payload["sku"] is not None:
        item.sku = payload["sku"]
    if "name" in payload and payload["name"] is not None:
        item.name = payload["name"]
    if "description" in payload:
        item.description = payload["description"]
    if "quantity" in payload and payload["quantity"] is not None:
        item.quantity = payload["quantity"]
    if "min_quantity" in payload and payload["min_quantity"] is not None:
        item.min_quantity = payload["min_quantity"]
    if "location" in payload:
        item.location = payload["location"]
    if "price" in payload and payload["price"] is not None:
        item.price = Decimal(str(payload["price"]))
    if "status" in payload and payload["status"] is not None:
        item.status = ItemStatus(payload["status"])
    if "category_id" in payload:
        item.category_id = payload["category_id"]

    db.commit()
    db.refresh(item)
    return get_item(db, item.id)


def delete_item(db: Session, item_id: str) -> None:
    item = get_item(db, item_id)
    db.delete(item)
    db.commit()


def summary(db: Session) -> dict:
    total_items = db.query(func.count(Item.id)).scalar() or 0
    low_stock_items = db.query(func.count(Item.id)).filter(Item.status == ItemStatus.LOW_STOCK).scalar() or 0
    out_of_stock_items = db.query(func.count(Item.id)).filter(Item.status == ItemStatus.OUT_OF_STOCK).scalar() or 0
    total_categories = db.query(func.count(Category.id)).scalar() or 0
    return {
        "totalItems": total_items,
        "lowStockItems": low_stock_items,
        "outOfStockItems": out_of_stock_items,
        "totalCategories": total_categories,
    }
