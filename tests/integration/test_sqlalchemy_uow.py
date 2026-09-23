from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from proyecto_final.application.dtos import (
    CreateOrderCommand,
    CreateOrderItemData,
)
from proyecto_final.application.use_cases import (
    CreateOrder,
    GetOrder,
)
from proyecto_final.infrastructure.database.base import (
    Base,
)
from proyecto_final.infrastructure.notifications.memory import (
    MemoryNotificationAdapter,
)
from proyecto_final.infrastructure.unit_of_work.sqlalchemy import (
    SQLAlchemyUnitOfWork,
)


def test_create_order_is_persisted() -> None:
    engine = create_engine(
        "sqlite://",
        connect_args={
            "check_same_thread": False,
        },
        poolclass=StaticPool,
    )

    Base.metadata.create_all(engine)

    test_session_factory: sessionmaker[Session] = sessionmaker(
        bind=engine,
        expire_on_commit=False,
    )

    uow = SQLAlchemyUnitOfWork(test_session_factory)

    notification = MemoryNotificationAdapter()

    create_order = CreateOrder(
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

    create_order.execute(command)

    uow.close()

    second_uow = SQLAlchemyUnitOfWork(test_session_factory)

    get_order = GetOrder(second_uow.orders)

    order = get_order.execute(1)

    assert order.id == 1
    assert order.customer == "Cesar"
    assert order.total == Decimal("15000.00")

    second_uow.close()

    Base.metadata.drop_all(engine)
    engine.dispose()
