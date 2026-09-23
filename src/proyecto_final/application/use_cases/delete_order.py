from proyecto_final.application.ports import (
    UnitOfWork,
)
from proyecto_final.domain.exceptions import (
    OrderNotFoundError,
)


class DeleteOrder:
    def __init__(
        self,
        uow: UnitOfWork,
    ) -> None:
        self.uow = uow

    def execute(
        self,
        order_id: int,
    ) -> None:
        try:
            deleted = self.uow.orders.delete(order_id)

            if not deleted:
                raise OrderNotFoundError(f"La orden {order_id} no existe")

            self.uow.commit()

        except Exception:
            self.uow.rollback()
            raise
