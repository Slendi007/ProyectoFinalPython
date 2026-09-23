class DomainError(Exception):
    "____Error base del dominio.____"


class InvalidQuantityError(DomainError):
    "____La cantidad de un producto no es válida____"


class InvalidPriceError(DomainError):
    "____El precio de un producto no es válido____"


class EmptyOrderError(DomainError):
    "____La orden no contiene productos.____"


class OrderNotFoundError(DomainError):
    "____La orden solicitada no existe____"
