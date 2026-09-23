from datetime import UTC, datetime

from proyecto_final.application.dtos import CreateOrderCommand
from proyecto_final.application.ports import (
    NotificationPort,
    UnitOfWork,
)
from proyecto_final.domain.entities import (
    Order,
    OrderItem,
)
from proyecto_final.domain.events import OrderCreated


class CreateOrder:
    def __init__(
        self,
        uow: UnitOfWork,
        notification: NotificationPort,
    ) -> None:
        self.uow = uow
        self.notification = notification

    def execute(
        self,
        command: CreateOrderCommand,
    ) -> Order:
        order = Order(
            id=command.order_id,
            customer=command.customer,
        )

        for item_data in command.items:
            item = OrderItem(
                product=item_data.product,
                quantity=item_data.quantity,
                unit_price=item_data.unit_price,
            )

            order.add_item(item)

        order.validate()

        try:
            self.uow.orders.add(order)
            self.uow.commit()

        except Exception:
            self.uow.rollback()
            raise

        event = OrderCreated(
            order_id=order.id,
            customer=order.customer,
            occurred_at=datetime.now(UTC),
        )

        self.notification.notify_order_created(event)

        return order
