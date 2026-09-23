from getpass import getpass

from sqlalchemy import select

from proyecto_final.infrastructure.database import (
    SessionLocal,
)
from proyecto_final.infrastructure.database.models import (
    UserModel,
)
from proyecto_final.infrastructure.security.passwords import (
    PasswordService,
)


def main() -> None:
    username = input("Usuario: ").strip()

    password = getpass("Contraseña: ")

    confirm_password = getpass("Confirma la contraseña: ")

    if not username:
        print("El usuario no puede estar vacío.")
        return

    if not password:
        print("La contraseña no puede estar vacía.")
        return

    if password != confirm_password:
        print("Las contraseñas no coinciden.")
        return

    password_service = PasswordService()

    with SessionLocal() as session:
        existing_user = session.scalar(
            select(UserModel).where(UserModel.username == username)
        )

        if existing_user is not None:
            print("El usuario ya existe.")
            return

        user = UserModel(
            username=username,
            password_hash=(password_service.hash(password)),
        )

        session.add(user)
        session.commit()

    print(f"Usuario '{username}' creado.")


if __name__ == "__main__":
    main()
