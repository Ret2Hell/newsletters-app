import logging

from app.config import settings
from sqlmodel import Session, SQLModel, create_engine

logger = logging.getLogger(__name__)


try:
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=True,
    )
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    raise


def create_db_and_tables():
    try:
        SQLModel.metadata.create_all(engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise


def get_session():
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Session error: {e}")
            session.rollback()
            raise
