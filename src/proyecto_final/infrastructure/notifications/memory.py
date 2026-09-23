from proyecto_final.domain.events import (
    OrderCreated,
)


class MemoryNotificationAdapter:
    def __init__(self) -> None:
        self.events: list[OrderCreated] = []

    def notify_order_created(
        self,
        event: OrderCreated,
    ) -> None:
        self.events.append(event)
