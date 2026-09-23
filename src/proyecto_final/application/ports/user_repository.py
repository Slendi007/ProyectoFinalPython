from typing import Protocol

from proyecto_final.domain.entities import User


class UserRepository(Protocol):
    def get_by_username(
        self,
        username: str,
    ) -> User | None: ...
