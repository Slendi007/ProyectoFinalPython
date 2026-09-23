from proyecto_final.application.exceptions import (
    InvalidCredentialsError,
)
from proyecto_final.application.ports import (
    PasswordHasher,
    UserRepository,
)
from proyecto_final.domain.entities import User


class AuthenticateUser:
    def __init__(
        self,
        repository: UserRepository,
        password_hasher: PasswordHasher,
    ) -> None:
        self.repository = repository
        self.password_hasher = password_hasher

    def execute(
        self,
        username: str,
        password: str,
    ) -> User:
        user = self.repository.get_by_username(username)

        if user is None:
            raise InvalidCredentialsError("Usuario o contraseña incorrectos!")

        if not self.password_hasher.verify(
            password,
            user.password_hash,
        ):
            raise InvalidCredentialsError("Usuario o contraseña incorrectos!")

        return user
