from datetime import UTC, datetime, timedelta

import jwt

from proyecto_final.infrastructure.config import (
    get_settings,
)


class TokenValidationError(Exception):
    "____El token JWT no es válido._____"


class JWTService:
    def __init__(self) -> None:
        settings = get_settings()

        if settings.jwt_secret_key is None:
            raise RuntimeError("JWT_SECRET_KEY no está configurada!")

        self.secret_key = settings.jwt_secret_key.get_secret_value()
        self.algorithm = settings.jwt_algorithm
        self.access_token_minutes = settings.access_token_minutes

    def create_access_token(
        self,
        subject: str,
    ) -> str:
        expires_at = datetime.now(UTC) + timedelta(minutes=self.access_token_minutes)

        payload = {
            "sub": subject,
            "exp": expires_at,
        }

        return jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm,
        )

    def decode_access_token(
        self,
        token: str,
    ) -> str:
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[
                    self.algorithm,
                ],
            )

            subject = payload.get("sub")

            if not isinstance(subject, str):
                raise TokenValidationError("Token inválido!")

            return subject

        except jwt.InvalidTokenError as exc:
            raise TokenValidationError("Token inválido o expirado!") from exc
