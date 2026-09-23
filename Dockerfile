
# Etapa 1: Builder


FROM python:3.14-slim AS builder

ENV POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock README.md ./

RUN poetry install \
    --only main \
    --no-root \
    --no-ansi

COPY src ./src

RUN poetry install \
    --only main \
    --no-ansi


# Etapa 2: Runtime

FROM python:3.14-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN groupadd --system appgroup \
    && useradd \
        --system \
        --gid appgroup \
        --create-home \
        appuser \
    && chown appuser:appgroup /app

COPY --from=builder \
    --chown=appuser:appgroup \
    /app/.venv \
    /app/.venv

COPY --chown=appuser:appgroup \
    src \
    ./src

COPY --chown=appuser:appgroup \
    alembic \
    ./alembic

COPY --chown=appuser:appgroup \
    alembic.ini \
    ./

USER appuser

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn proyecto_final.api.main:app --host 0.0.0.0 --port 8000"]