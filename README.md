# Proyecto Final - Orders API

Servicio REST para gestión de órdenes desarrollado con Python y FastAPI aplicando principios de Arquitectura Hexagonal y Arquitectura Limpia.

## Objetivos

El proyecto tiene como objetivos:

- Construir un servicio de Orders separado en dominio, aplicación e infraestructura.
- Aplicar puertos y adaptadores.
- Exponer una API REST utilizando FastAPI.
- Implementar autenticación mediante JWT.
- Persistir información utilizando SQLAlchemy.
- Gestionar migraciones con Alembic.
- Implementar pruebas unitarias, de contrato, integración y E2E.
- Aplicar análisis de calidad con Ruff, mypy y pytest.
- Auditar dependencias.
- Empaquetar la aplicación mediante Docker.
- Automatizar validaciones y entrega con GitHub Actions.

## Tecnologías

- Python 3.14
- FastAPI
- Pydantic
- pydantic-settings
- SQLAlchemy
- Alembic
- SQLite
- PyJWT
- pwdlib / Argon2
- pytest
- pytest-cov
- Ruff
- mypy
- pip-audit
- Poetry
- Docker
- GitHub Actions

## Arquitectura

El proyecto está organizado utilizando Arquitectura Hexagonal/Limpia.

```text
API
 │
 ▼
Application
 │
 ▼
Domain
 ▲
 │
Ports
 ▲
 │
Infrastructure
```

Las principales capas son:

### Domain

Contiene las reglas de negocio y no depende de FastAPI, SQLAlchemy ni otras tecnologías externas.

Incluye:

- Order
- OrderItem
- OrderCreated
- Excepciones de dominio

### Application

Contiene los casos de uso y los puertos.

Casos de uso principales:

- CreateOrder
- GetOrder
- ListOrders
- DeleteOrder
- AuthenticateUser

Puertos principales:

- OrderRepository
- UserRepository
- UnitOfWork
- NotificationPort
- PasswordHasher

### Infrastructure

Contiene las implementaciones concretas de los puertos:

- SQLAlchemyOrderRepository
- SQLAlchemyUserRepository
- SQLAlchemyUnitOfWork
- SQLite
- JWTService
- PasswordService
- Adaptadores de notificación

### API

Implementada con FastAPI.

Se encarga de:

- Recibir peticiones HTTP.
- Validar datos con Pydantic.
- Resolver dependencias.
- Ejecutar casos de uso.
- Convertir excepciones a respuestas HTTP.

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/Slendi007/ProyectoFinalPython.git
cd proyecto_final
```

Instalar las dependencias:

```bash
poetry install
```

## Configuración

Copiar:

```text
.env.example
```

como:

```text
.env
```

Ejemplo:

```env
APP_NAME=Proyecto Final - Orders API
APP_VERSION=1.0.0
DEBUG=false

DATABASE_URL=sqlite:///./orders.db

JWT_SECRET_KEY=cambiar-por-una-clave-segura
JWT_ALGORITHM=HS256
ACCESS_TOKEN_MINUTES=30
```

Se puede generar una clave JWT mediante:

```bash
poetry run python -c "import secrets; print(secrets.token_urlsafe(32))"
```

El archivo `.env` no debe almacenarse en Git.

## Migraciones

Aplicar las migraciones:

```bash
poetry run alembic upgrade head
```

Consultar la migración actual:

```bash
poetry run alembic current
```

Consultar historial:

```bash
poetry run alembic history
```

## Crear usuario

Crear un usuario para acceder a la API:

```bash
poetry run python -m proyecto_final.infrastructure.security.create_user
```

El script solicitará:

```text
Usuario:
Contraseña:
Confirma la contraseña:
```

Las contraseñas se almacenan utilizando hash y no en texto plano.

## Ejecutar la API

```bash
poetry run uvicorn proyecto_final.api.main:app --reload
```

La API estará disponible en:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

## Endpoints

### Health

```text
GET /health
```

### Autenticación

```text
POST /auth/login
```

Devuelve un JWT Bearer Token.

### Orders

Los endpoints de órdenes requieren autenticación.

```text
POST   /orders
GET    /orders
GET    /orders/{order_id}
DELETE /orders/{order_id}
```

Ejemplo de creación:

```json
{
  "id": 1,
  "customer": "Cesar",
  "items": [
    {
      "product": "Laptop",
      "quantity": 1,
      "unit_price": 15000
    },
    {
      "product": "Mouse",
      "quantity": 2,
      "unit_price": 350
    }
  ]
}
```

## Pruebas

Ejecutar todas las pruebas:

```bash
poetry run pytest
```

El proyecto contiene:

```text
tests/
├── unit/
├── contract/
├── integration/
└── e2e/
```

### Unitarias

Prueban entidades y casos de uso de forma aislada.

### Contrato

Comprueban que diferentes implementaciones de repositorios respeten el mismo contrato.

### Integración

Comprueban la integración de SQLAlchemy, UnitOfWork, repositorios y SQLite.

### E2E

Comprueban el flujo completo:

```text
Login
  ↓
JWT
  ↓
Crear Order
  ↓
Consultar
  ↓
Listar
  ↓
Eliminar
```

## Cobertura

Ejecutar:

```bash
poetry run pytest --cov=proyecto_final --cov-report=term-missing
```

Reporte HTML:

```bash
poetry run pytest --cov=proyecto_final --cov-report=html
```

## Calidad de código

Formato:

```bash
poetry run ruff format --check .
```

Lint:

```bash
poetry run ruff check .
```

Tipado:

```bash
poetry run mypy src/proyecto_final
```

## Auditoría de dependencias

Ejecutar:

```bash
poetry run pip-audit
```

La evidencia se encuentra en:

```text
docs/evidence/
```

## Docker

Construir la imagen:

```bash
docker build -t proyecto-final-orders .
```

Ejecutar:

```bash
docker run --rm -d \
  --name proyecto-final-api \
  -p 8000:8000 \
  --env-file .env \
  proyecto-final-orders
```

En PowerShell se puede ejecutar en una sola línea:

```powershell
docker run --rm -d --name proyecto-final-api -p 8000:8000 --env-file .env proyecto-final-orders
```

Comprobar que el proceso no se ejecuta como root:

```bash
docker exec proyecto-final-api whoami
```

Resultado esperado:

```text
appuser
```

## CI/CD

El pipeline de GitHub Actions está definido en:

```text
.github/workflows/ci.yml
```

Ejecuta automáticamente:

```text
Ruff
 ↓
mypy
 ↓
pytest + coverage
 ↓
pip-audit
 ↓
Docker build
 ↓
GitHub Container Registry
```

La imagen Docker solamente se publica si las validaciones anteriores terminan correctamente.

## Diagramas

Los diagramas de arquitectura se encuentran en:

```text
docs/diagrams/
```

- `architecture.md`
- `request-flow.md`

## Seguridad

El proyecto incluye:

- Contraseñas con hash Argon2.
- Autenticación JWT.
- Bearer authentication.
- Configuración mediante variables de entorno.
- `.env` excluido de Git.
- Auditoría de dependencias.
- Imagen Docker ejecutada como usuario no-root.
- Separación entre dominio e infraestructura.

## Estructura de pruebas

```text
Unitarias
    ↓
Contrato
    ↓
Integración
    ↓
E2E
```

Esta combinación permite validar desde las reglas de negocio más pequeñas hasta el flujo completo de la API.