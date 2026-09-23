from sqlalchemy import select
from sqlalchemy.orm import Session

from proyecto_final.domain.entities import User
from proyecto_final.infrastructure.database.models import (
    UserModel,
)


class SQLAlchemyUserRepository:
    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session

    def get_by_username(
        self,
        username: str,
    ) -> User | None:
        statement = select(UserModel).where(UserModel.username == username)

        model = self.session.scalar(statement)

        if model is None:
            return None

        return User(
            id=model.id,
            username=model.username,
            password_hash=model.password_hash,
        )
