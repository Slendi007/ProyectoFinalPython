from dataclasses import dataclass, field
from decimal import Decimal

from ..exceptions import EmptyOrderError
from .order_item import OrderItem


@dataclass
class Order:
    id: int
    customer: str
    items: list[OrderItem] = field(
        default_factory=list,
    )

    def add_item(
        self,
        item: OrderItem,
    ) -> None:
        self.items.append(item)

    @property
    def total(self) -> Decimal:
        return sum(
            (item.subtotal for item in self.items),
            Decimal(0),
        )

    def validate(self) -> None:
        if not self.items:
            raise EmptyOrderError("La orden debe contener al menos un producto!")
