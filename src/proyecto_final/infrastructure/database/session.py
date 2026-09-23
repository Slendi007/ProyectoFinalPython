from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

DATABASE_URL = "sqlite:///./orders.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
)

SessionLocal: sessionmaker[Session] = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)
