from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from proyecto_final.api.dependencies import (
    get_uow,
    get_user_repository,
)
from proyecto_final.api.main import app
from proyecto_final.infrastructure.database.base import Base
from proyecto_final.infrastructure.database.models import (
    UserModel,
)
from proyecto_final.infrastructure.repositories import (
    SQLAlchemyUserRepository,
)
from proyecto_final.infrastructure.security.passwords import (
    PasswordService,
)
from proyecto_final.infrastructure.unit_of_work import (
    SQLAlchemyUnitOfWork,
)


@pytest.fixture
def client(
    monkeypatch: pytest.MonkeyPatch,
) -> Generator[TestClient]:
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        "clave-secreta-exclusiva-para-tests",
    )

    engine = create_engine(
        "sqlite://",
        connect_args={
            "check_same_thread": False,
        },
        poolclass=StaticPool,
    )

    Base.metadata.create_all(engine)

    session_factory = sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )

    password_service = PasswordService()

    with session_factory() as session:
        admin = UserModel(
            username="admin",
            password_hash=password_service.hash("admin123"),
        )

        session.add(admin)
        session.commit()

    def override_get_uow() -> Generator[SQLAlchemyUnitOfWork]:
        uow = SQLAlchemyUnitOfWork(session_factory)

        try:
            yield uow
        finally:
            uow.close()

    def override_get_user_repository() -> Generator[SQLAlchemyUserRepository]:
        session = session_factory()

        try:
            yield SQLAlchemyUserRepository(session)
        finally:
            session.close()

    app.dependency_overrides[get_uow] = override_get_uow

    app.dependency_overrides[get_user_repository] = override_get_user_repository

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

    Base.metadata.drop_all(engine)
    engine.dispose()
