import os
from datetime import UTC, datetime, timedelta

import jwt


class TokenValidationError(Exception):
    "_______El token JWT no es válido______"


class JWTService:
    ALGORITHM = "HS256"
    ACCESS_TOKEN_MINUTES = 30

    def __init__(self) -> None:
        secret_key = os.getenv("JWT_SECRET_KEY")

        if not secret_key:
            raise RuntimeError("JWT_SECRET_KEY no está configurada!")

        self.secret_key = secret_key

    def create_access_token(
        self,
        subject: str,
    ) -> str:
        expires_at = datetime.now(UTC) + timedelta(minutes=self.ACCESS_TOKEN_MINUTES)

        payload = {
            "sub": subject,
            "exp": expires_at,
        }

        return jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.ALGORITHM,
        )

    def decode_access_token(
        self,
        token: str,
    ) -> str:
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.ALGORITHM],
            )

            subject = payload.get("sub")

            if not isinstance(
                subject,
                str,
            ):
                raise TokenValidationError("Token inválido!")

            return subject

        except jwt.InvalidTokenError as exc:
            raise TokenValidationError("Token inválido o expirado!") from exc


# clave secreta: GR6xiVofhso0fypmR-YnQAXLWjyF2F9LygeZz4kyfBE
