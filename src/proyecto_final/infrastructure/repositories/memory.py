from proyecto_final.domain.entities import Order


class MemoryOrderRepository:
    def __init__(self) -> None:
        self._orders: dict[int, Order] = {}

    def add(
        self,
        order: Order,
    ) -> None:
        self._orders[order.id] = order

    def get(
        self,
        order_id: int,
    ) -> Order | None:
        return self._orders.get(order_id)

    def list_all(self) -> list[Order]:
        return list(self._orders.values())

    def delete(
        self,
        order_id: int,
    ) -> bool:
        if order_id not in self._orders:
            return False

        del self._orders[order_id]

        return True
