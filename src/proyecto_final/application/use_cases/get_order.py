from proyecto_final.application.ports import (
    OrderRepository,
)
from proyecto_final.domain.entities import Order
from proyecto_final.domain.exceptions import (
    OrderNotFoundError,
)


class GetOrder:
    def __init__(
        self,
        repository: OrderRepository,
    ) -> None:
        self.repository = repository

    def execute(
        self,
        order_id: int,
    ) -> Order:
        order = self.repository.get(order_id)

        if order is None:
            raise OrderNotFoundError(f"La orden {order_id} no existe")

        return order
