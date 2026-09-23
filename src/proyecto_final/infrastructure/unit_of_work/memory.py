from proyecto_final.application.ports import (
    OrderRepository,
)
from proyecto_final.infrastructure.repositories.memory import (
    MemoryOrderRepository,
)


class MemoryUnitOfWork:
    def __init__(self) -> None:
        self.orders: OrderRepository = MemoryOrderRepository()

        self.committed = False
        self.rolled_back = False

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        self.rolled_back = True
