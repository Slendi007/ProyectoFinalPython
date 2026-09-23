from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class OrderItemCreate(BaseModel):
    product: str = Field(
        min_length=1,
        max_length=200,
    )
    quantity: int = Field(gt=0)
    unit_price: Decimal = Field(ge=0)


class OrderCreate(BaseModel):
    id: int = Field(gt=0)
    customer: str = Field(
        min_length=1,
        max_length=150,
    )
    items: list[OrderItemCreate] = Field(
        min_length=1,
    )


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    product: str
    quantity: int
    unit_price: Decimal
    subtotal: Decimal


class OrderResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    customer: str
    items: list[OrderItemResponse]
    total: Decimal


class MessageResponse(BaseModel):
    message: str
