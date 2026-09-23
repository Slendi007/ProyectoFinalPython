from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from proyecto_final.api.routes import (
    auth_router,
    orders_router,
)
from proyecto_final.domain.exceptions import (
    DomainError,
    OrderNotFoundError,
)
from proyecto_final.infrastructure.config import (
    get_settings,
)

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description=("Servicio de órdenes utilizando Arquitectura Hexagonal y Limpia."),
    version=settings.app_version,
    debug=settings.debug,
)

app.include_router(auth_router)
app.include_router(orders_router)


@app.exception_handler(OrderNotFoundError)
async def order_not_found_handler(
    _request: Request,
    exc: OrderNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": str(exc),
        },
    )


@app.exception_handler(DomainError)
async def domain_error_handler(
    _request: Request,
    exc: DomainError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": str(exc),
        },
    )


@app.get(
    "/health",
    tags=["Health"],
)
def health() -> dict[str, str]:
    return {
        "status": "ok",
    }


app.include_router(orders_router)
