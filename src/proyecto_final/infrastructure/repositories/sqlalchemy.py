from sqlalchemy import select
from sqlalchemy.orm import Session

from proyecto_final.domain.entities import (
    Order,
    OrderItem,
)
from proyecto_final.infrastructure.database.models import (
    OrderItemModel,
    OrderModel,
)


class SQLAlchemyOrderRepository:
    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session

    def add(
        self,
        order: Order,
    ) -> None:
        model = OrderModel(
            id=order.id,
            customer=order.customer,
            items=[
                OrderItemModel(
                    product=item.product,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                )
                for item in order.items
            ],
        )

        self.session.add(model)
        self.session.flush()

    def get(
        self,
        order_id: int,
    ) -> Order | None:
        model = self.session.get(
            OrderModel,
            order_id,
        )

        if model is None:
            return None

        return self._to_domain(model)

    def list_all(self) -> list[Order]:
        statement = select(OrderModel).order_by(OrderModel.id)

        models = self.session.scalars(statement).all()

        return [self._to_domain(model) for model in models]

    def delete(
        self,
        order_id: int,
    ) -> bool:
        model = self.session.get(
            OrderModel,
            order_id,
        )

        if model is None:
            return False

        self.session.delete(model)
        self.session.flush()

        return True

    @staticmethod
    def _to_domain(
        model: OrderModel,
    ) -> Order:
        return Order(
            id=model.id,
            customer=model.customer,
            items=[
                OrderItem(
                    product=item.product,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                )
                for item in model.items
            ],
        )
