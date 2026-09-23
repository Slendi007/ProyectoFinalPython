from decimal import Decimal

import pytest

from proyecto_final.application.dtos import (
    CreateOrderCommand,
    CreateOrderItemData,
)
from proyecto_final.application.use_cases import (
    CreateOrder,
    DeleteOrder,
    GetOrder,
    ListOrders,
)
from proyecto_final.domain.exceptions import (
    OrderNotFoundError,
)
from proyecto_final.infrastructure.notifications.memory import (
    MemoryNotificationAdapter,
)
from proyecto_final.infrastructure.unit_of_work.memory import (
    MemoryUnitOfWork,
)


def crear_order(
    uow: MemoryUnitOfWork,
) -> None:
    notification = MemoryNotificationAdapter()

    use_case = CreateOrder(
        uow,
        notification,
    )

    command = CreateOrderCommand(
        order_id=1,
        customer="Cesar",
        items=[
            CreateOrderItemData(
                product="Laptop",
                quantity=1,
                unit_price=Decimal("15000.00"),
            )
        ],
    )

    use_case.execute(command)


def test_get_order() -> None:
    uow = MemoryUnitOfWork()

    crear_order(uow)

    use_case = GetOrder(uow.orders)

    order = use_case.execute(1)

    assert order.id == 1


def test_list_orders() -> None:
    uow = MemoryUnitOfWork()

    crear_order(uow)

    use_case = ListOrders(uow.orders)

    orders = use_case.execute()

    assert len(orders) == 1


def test_delete_order() -> None:
    uow = MemoryUnitOfWork()

    crear_order(uow)

    use_case = DeleteOrder(uow)

    use_case.execute(1)

    assert uow.orders.get(1) is None


def test_get_missing_order() -> None:
    uow = MemoryUnitOfWork()

    use_case = GetOrder(uow.orders)

    with pytest.raises(
        OrderNotFoundError,
    ):
        use_case.execute(999)
