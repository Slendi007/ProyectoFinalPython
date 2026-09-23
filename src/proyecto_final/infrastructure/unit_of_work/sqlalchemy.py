from sqlalchemy.orm import Session, sessionmaker

from proyecto_final.application.ports import (
    OrderRepository,
)
from proyecto_final.infrastructure.database import (
    SessionLocal,
)
from proyecto_final.infrastructure.repositories import (
    SQLAlchemyOrderRepository,
)


class SQLAlchemyUnitOfWork:
    def __init__(
        self,
        session_factory: sessionmaker[Session] = SessionLocal,
    ) -> None:
        self.session = session_factory()

        self.orders: OrderRepository = SQLAlchemyOrderRepository(self.session)

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

    def close(self) -> None:
        self.session.close()
