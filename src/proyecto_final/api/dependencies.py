from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from proyecto_final.infrastructure.database import SessionLocal
from proyecto_final.infrastructure.repositories import (
    SQLAlchemyUserRepository,
)
from proyecto_final.infrastructure.security.jwt_service import (
    JWTService,
    TokenValidationError,
)
from proyecto_final.infrastructure.unit_of_work import (
    SQLAlchemyUnitOfWork,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_uow() -> Generator[SQLAlchemyUnitOfWork]:
    uow = SQLAlchemyUnitOfWork()

    try:
        yield uow
    finally:
        uow.close()


def get_user_repository() -> Generator[SQLAlchemyUserRepository]:
    session = SessionLocal()

    try:
        yield SQLAlchemyUserRepository(session)
    finally:
        session.close()


def get_current_user(
    token: Annotated[
        str,
        Depends(oauth2_scheme),
    ],
) -> str:
    try:
        return JWTService().decode_access_token(token)

    except TokenValidationError as exc:
        raise HTTPException(
            status_code=(status.HTTP_401_UNAUTHORIZED),
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
