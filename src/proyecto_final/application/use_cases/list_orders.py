from proyecto_final.application.ports import (
    OrderRepository,
)
from proyecto_final.domain.entities import Order


class ListOrders:
    def __init__(
        self,
        repository: OrderRepository,
    ) -> None:
        self.repository = repository

    def execute(self) -> list[Order]:
        return self.repository.list_all()
