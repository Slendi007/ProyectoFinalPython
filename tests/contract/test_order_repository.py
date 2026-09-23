from collections.abc import Generator
from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from proyecto_final.application.ports import OrderRepository
from proyecto_final.domain.entities import Order, OrderItem
from proyecto_final.infrastructure.database.base import Base
from proyecto_final.infrastructure.repositories import (
    MemoryOrderRepository,
    SQLAlchemyOrderRepository,
)


@pytest.fixture(
    params=[
        "memory",
        "sqlalchemy",
    ]
)
def repository(
    request: pytest.FixtureRequest,
) -> Generator[OrderRepository]:
    if request.param == "memory":
        yield MemoryOrderRepository()
        return

    engine = create_engine(
        "sqlite://",
        connect_args={
            "check_same_thread": False,
        },
        poolclass=StaticPool,
    )

    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield SQLAlchemyOrderRepository(session)

    Base.metadata.drop_all(engine)
    engine.dispose()


def crear_order() -> Order:
    return Order(
        id=1,
        customer="Cesar",
        items=[
            OrderItem(
                product="Laptop",
                quantity=1,
                unit_price=Decimal("15000.00"),
            ),
            OrderItem(
                product="Mouse",
                quantity=2,
                unit_price=Decimal("350.00"),
            ),
        ],
    )


def test_repository_add_and_get(
    repository: OrderRepository,
) -> None:
    order = crear_order()

    repository.add(order)

    saved = repository.get(1)

    assert saved is not None
    assert saved.id == 1
    assert saved.customer == "Cesar"
    assert saved.total == Decimal("15700.00")


def test_repository_list_all(
    repository: OrderRepository,
) -> None:
    repository.add(crear_order())

    orders = repository.list_all()

    assert len(orders) == 1


def test_repository_delete(
    repository: OrderRepository,
) -> None:
    repository.add(crear_order())

    deleted = repository.delete(1)

    assert deleted is True
    assert repository.get(1) is None


def test_repository_delete_missing(
    repository: OrderRepository,
) -> None:
    deleted = repository.delete(999)

    assert deleted is False
