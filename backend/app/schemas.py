from decimal import Decimal
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


def to_camel(value: str) -> str:
    parts = value.split("_")
    return parts[0] + "".join(part.capitalize() for part in parts[1:])


class CamelModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )


class TokenPayload(CamelModel):
    sub: str
    role: str
    email: str


class CategoryRead(CamelModel):
    id: str
    name: str


class UserRead(CamelModel):
    id: str
    email: EmailStr
    full_name: str
    role: str


class LoginRequest(CamelModel):
    email: EmailStr
    password: str = Field(min_length=6)


class LoginResponse(CamelModel):
    token: str
    user: UserRead


class ItemBase(CamelModel):
    sku: str = Field(min_length=2)
    name: str = Field(min_length=2)
    description: str | None = None
    quantity: int = 0
    min_quantity: int = 0
    location: str | None = None
    price: Decimal = Decimal("0")
    status: Literal["ACTIVE", "LOW_STOCK", "OUT_OF_STOCK", "DISCONTINUED"] = "ACTIVE"
    category_id: str | None = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(CamelModel):
    sku: str | None = None
    name: str | None = None
    description: str | None = None
    quantity: int | None = None
    min_quantity: int | None = None
    location: str | None = None
    price: Decimal | None = None
    status: Literal["ACTIVE", "LOW_STOCK", "OUT_OF_STOCK", "DISCONTINUED"] | None = None
    category_id: str | None = None


class ItemRead(CamelModel):
    id: str
    sku: str
    name: str
    description: str | None
    quantity: int
    min_quantity: int
    location: str | None
    price: Decimal
    status: str
    updated_at: datetime | None = None
    category: CategoryRead | None = None
    created_by: UserRead | None = None


class SummaryRead(CamelModel):
    total_items: int
    low_stock_items: int
    out_of_stock_items: int
    total_categories: int


class ApiResponse(CamelModel):
    success: bool = True
    data: object
