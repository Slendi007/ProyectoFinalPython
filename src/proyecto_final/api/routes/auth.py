from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.security import (
    OAuth2PasswordRequestForm,
)

from proyecto_final.api.dependencies import (
    get_user_repository,
)
from proyecto_final.api.schemas.auth import (
    TokenResponse,
)
from proyecto_final.application.exceptions import (
    InvalidCredentialsError,
)
from proyecto_final.application.use_cases.authenticate_user import (
    AuthenticateUser,
)
from proyecto_final.infrastructure.repositories import (
    SQLAlchemyUserRepository,
)
from proyecto_final.infrastructure.security.jwt_service import (
    JWTService,
)
from proyecto_final.infrastructure.security.passwords import (
    PasswordService,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

UserRepositoryDependency = Annotated[
    SQLAlchemyUserRepository,
    Depends(get_user_repository),
]


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    form_data: Annotated[
        OAuth2PasswordRequestForm,
        Depends(),
    ],
    repository: UserRepositoryDependency,
) -> TokenResponse:
    use_case = AuthenticateUser(
        repository=repository,
        password_hasher=PasswordService(),
    )

    try:
        user = use_case.execute(
            username=form_data.username,
            password=form_data.password,
        )

    except InvalidCredentialsError as exc:
        raise HTTPException(
            status_code=(status.HTTP_401_UNAUTHORIZED),
            detail=("Usuario o contraseña incorrectos"),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    token = JWTService().create_access_token(subject=user.username)

    return TokenResponse(
        access_token=token,
        token_type="bearer",
    )
