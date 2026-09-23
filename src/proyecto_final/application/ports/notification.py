from typing import Protocol

from proyecto_final.domain.events import OrderCreated


class NotificationPort(Protocol):
    def notify_order_created(
        self,
        event: OrderCreated,
    ) -> None: ...
