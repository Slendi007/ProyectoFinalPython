import pytest

from proyecto_final.domain.exceptions import (
    EmptyOrderError,
)

from decimal import Decimal

from proyecto_final.application.dtos import (
    CreateOrderCommand,
    CreateOrderItemData,
)
from proyecto_final.application.use_cases import (
    CreateOrder,
)
from proyecto_final.infrastructure.notifications.memory import (
    MemoryNotificationAdapter,
)
from proyecto_final.infrastructure.unit_of_work.memory import (
    MemoryUnitOfWork,
)


def test_create_order() -> None:
    uow = MemoryUnitOfWork()

    notification = MemoryNotificationAdapter()

    use_case = CreateOrder(
        uow=uow,
        notification=notification,
    )

    command = CreateOrderCommand(
        order_id=1,
        customer="Cesar",
        items=[
            CreateOrderItemData(
                product="Laptop",
                quantity=1,
                unit_price=Decimal("15000.00"),
            ),
            CreateOrderItemData(
                product="Mouse",
                quantity=2,
                unit_price=Decimal("350.00"),
            ),
        ],
    )

    order = use_case.execute(command)

    assert order.id == 1
    assert order.customer == "Cesar"

    assert order.total == Decimal("15700.00")

    assert uow.committed is True

    saved_order = uow.orders.get(1)

    assert saved_order == order

    assert len(notification.events) == 1

    assert notification.events[0].order_id == 1


def test_create_empty_order_fails() -> None:
    uow = MemoryUnitOfWork()

    notification = MemoryNotificationAdapter()

    use_case = CreateOrder(
        uow,
        notification,
    )

    command = CreateOrderCommand(
        order_id=1,
        customer="Cesar",
        items=[],
    )

    with pytest.raises(
        EmptyOrderError,
    ):
        use_case.execute(command)

    assert uow.committed is False

    assert len(notification.events) == 0
