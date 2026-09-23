from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class CreateOrderItemData:
    product: str
    quantity: int
    unit_price: Decimal


@dataclass(frozen=True)
class CreateOrderCommand:
    order_id: int
    customer: str
    items: list[CreateOrderItemData]
