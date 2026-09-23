from decimal import Decimal

import pytest

from proyecto_final.domain.entities import (
    Order,
    OrderItem,
)
from proyecto_final.domain.exceptions import (
    EmptyOrderError,
    InvalidPriceError,
    InvalidQuantityError,
)


def test_order_item_subtotal() -> None:
    item = OrderItem(
        product="Laptop",
        quantity=2,
        unit_price=Decimal("15000.00"),
    )

    assert item.subtotal == Decimal("30000.00")


def test_order_total() -> None:
    order = Order(
        id=1,
        customer="Cesar",
    )

    order.add_item(
        OrderItem(
            product="Laptop",
            quantity=1,
            unit_price=Decimal("15000.00"),
        )
    )

    order.add_item(
        OrderItem(
            product="Mouse",
            quantity=2,
            unit_price=Decimal("350.00"),
        )
    )

    assert order.total == Decimal("15700.00")


def test_quantity_must_be_positive() -> None:
    with pytest.raises(
        InvalidQuantityError,
    ):
        OrderItem(
            product="Mouse",
            quantity=0,
            unit_price=Decimal("350.00"),
        )


def test_price_cannot_be_negative() -> None:
    with pytest.raises(
        InvalidPriceError,
    ):
        OrderItem(
            product="Mouse",
            quantity=1,
            unit_price=Decimal("-10.00"),
        )


def test_order_cannot_be_empty() -> None:
    order = Order(
        id=1,
        customer="Cesar",
    )

    with pytest.raises(
        EmptyOrderError,
    ):
        order.validate()
