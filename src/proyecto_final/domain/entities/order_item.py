from dataclasses import dataclass
from decimal import Decimal

from ..exceptions import (
    InvalidPriceError,
    InvalidQuantityError,
)


@dataclass
class OrderItem:
    product: str
    quantity: int
    unit_price: Decimal

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise InvalidQuantityError("La cantidad debe ser mayor que cero!")

        if self.unit_price < 0:
            raise InvalidPriceError("El precio no puede ser negativo!")

    @property
    def subtotal(self) -> Decimal:
        return Decimal(self.quantity) * self.unit_price
