from typing import Protocol

from .order_repository import OrderRepository


class UnitOfWork(Protocol):
    orders: OrderRepository

    def commit(self) -> None: ...

    def rollback(self) -> None: ...
