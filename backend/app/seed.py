"""
Optional seed helper for local development.

Run manually after setting DATABASE_URL:
    python -m backend.app.seed
"""

from uuid import uuid4

from sqlalchemy.orm import Session

from .core.database import Base, SessionLocal, engine
from .core.security import hash_password
from .models import Category, Item, ItemStatus, Role, User


SEED_CATEGORIES = [
    "General",
    "Hardware",
    "Supplies",
    "Accessories",
]

SEED_ITEMS = [
    {
        "sku": "SKU-001",
        "name": "Sample Item",
        "description": "Starter inventory record",
        "quantity": 12,
        "min_quantity": 5,
        "location": "A-01",
        "price": 199.99,
        "status": ItemStatus.ACTIVE,
        "category": "General",
    },
    {
        "sku": "SKU-002",
        "name": "Wireless Scanner",
        "description": "Barcode scanner for warehouse work",
        "quantity": 8,
        "min_quantity": 3,
        "location": "H-02",
        "price": 2490.00,
        "status": ItemStatus.ACTIVE,
        "category": "Hardware",
    },
    {
        "sku": "SKU-003",
        "name": "Thermal Labels",
        "description": "Shipping labels for packing station",
        "quantity": 4,
        "min_quantity": 10,
        "location": "S-05",
        "price": 320.00,
        "status": ItemStatus.LOW_STOCK,
        "category": "Supplies",
    },
    {
        "sku": "SKU-004",
        "name": "Tablet Dock",
        "description": "Charging dock for stock tablets",
        "quantity": 0,
        "min_quantity": 2,
        "location": "H-07",
        "price": 1590.00,
        "status": ItemStatus.OUT_OF_STOCK,
        "category": "Accessories",
    },
]


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == "admin@inventory.local").one_or_none()
        if not admin:
            admin = User(
                id=uuid4().hex,
                email="admin@inventory.local",
                password_hash=hash_password("password123"),
                full_name="System Admin",
                role=Role.ADMIN,
            )
            db.add(admin)
            db.flush()

        categories: dict[str, Category] = {}
        for category_name in SEED_CATEGORIES:
            category = db.query(Category).filter(Category.name == category_name).one_or_none()
            if not category:
                category = Category(id=uuid4().hex, name=category_name)
                db.add(category)
                db.flush()
            categories[category_name] = category

        for item_data in SEED_ITEMS:
            exists = db.query(Item).filter(Item.sku == item_data["sku"]).one_or_none()
            if exists:
                continue

            category = categories[item_data["category"]]
            db.add(
                Item(
                    id=uuid4().hex,
                    sku=item_data["sku"],
                    name=item_data["name"],
                    description=item_data["description"],
                    quantity=item_data["quantity"],
                    min_quantity=item_data["min_quantity"],
                    location=item_data["location"],
                    price=item_data["price"],
                    status=item_data["status"],
                    category_id=category.id,
                    created_by_id=admin.id,
                )
            )

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
