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


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        if not db.query(User).filter(User.email == "admin@inventory.local").one_or_none():
            db.add(
                User(
                    id=uuid4().hex,
                    email="admin@inventory.local",
                    password_hash=hash_password("password123"),
                    full_name="System Admin",
                    role=Role.ADMIN,
                )
            )

        if not db.query(Category).filter(Category.name == "General").one_or_none():
            general = Category(id=uuid4().hex, name="General")
            db.add(general)
            db.flush()
            admin = db.query(User).filter(User.email == "admin@inventory.local").one()
            db.add(
                Item(
                    id=uuid4().hex,
                    sku="SKU-001",
                    name="Sample Item",
                    description="Starter inventory record",
                    quantity=12,
                    min_quantity=5,
                    location="A-01",
                    price=199.99,
                    status=ItemStatus.ACTIVE,
                    category_id=general.id,
                    created_by_id=admin.id,
                )
            )

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
