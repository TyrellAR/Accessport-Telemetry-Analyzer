from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.database.models import Base

DATABASE_URL = "sqlite:///./accessport_telemetry.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}

)

Sessionlocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

def init_db() -> None:
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Provide a database session to FastAPI endpoints."""
    db = Sessionlocal()

    try:
        yield db
    finally:
        db.close()