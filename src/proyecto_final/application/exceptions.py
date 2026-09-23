class ApplicationError(Exception):
    "____Error base de la capa de aplicación_____"


class InvalidCredentialsError(ApplicationError):
    "_____Usuario o contraseña incorrectos.____"
