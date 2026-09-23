import pytest

from proyecto_final.application.exceptions import (
    InvalidCredentialsError,
)
from proyecto_final.application.use_cases.authenticate_user import (
    AuthenticateUser,
)
from proyecto_final.domain.entities import User
from proyecto_final.infrastructure.security.passwords import (
    PasswordService,
)


class FakeUserRepository:
    def __init__(
        self,
        user: User | None,
    ) -> None:
        self.user = user

    def get_by_username(
        self,
        username: str,
    ) -> User | None:
        if self.user is not None and self.user.username == username:
            return self.user

        return None


def test_authenticate_user() -> None:
    password_service = PasswordService()

    user = User(
        id=1,
        username="admin",
        password_hash=password_service.hash("admin123"),
    )

    repository = FakeUserRepository(user)

    use_case = AuthenticateUser(
        repository=repository,
        password_hasher=password_service,
    )

    authenticated = use_case.execute(
        username="admin",
        password="admin123",
    )

    assert authenticated.username == "admin"


def test_authenticate_user_invalid_password() -> None:
    password_service = PasswordService()

    user = User(
        id=1,
        username="admin",
        password_hash=password_service.hash("admin123"),
    )

    repository = FakeUserRepository(user)

    use_case = AuthenticateUser(
        repository=repository,
        password_hasher=password_service,
    )

    with pytest.raises(
        InvalidCredentialsError,
    ):
        use_case.execute(
            username="admin",
            password="incorrecta",
        )
