"""
Database connection and session management.

This module handles SQLModel database initialization, table creation,
and provides session management for the application's database operations.
"""

import logging

from app.config import settings
from sqlmodel import Session, SQLModel, create_engine

logger = logging.getLogger(__name__)


try:
    # Create database engine with SQLite connection settings
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},  # SQLite-specific setting
        echo=True,  # Log all SQL queries for debugging
    )
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    raise


def create_db_and_tables():
    """
    Initialize the database by creating all tables defined in SQLModel classes.

    This function should be called during application startup to ensure
    the database schema is properly created before handling any requests.

    Raises:
        Exception: If table creation fails due to database connection issues,
                  insufficient permissions, or schema conflicts
    """
    try:
        SQLModel.metadata.create_all(engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise


def get_session():
    """
    Create and yield a database session for request handling.

    This is designed to be used as a FastAPI dependency to provide
    database sessions to route handlers. The session is automatically
    closed when the request is complete, and rolled back if an exception occurs.

    Yields:
        Session: SQLModel database session

    Raises:
        Exception: If session operations fail, after performing rollback
    """
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Session error: {e}")
            session.rollback()
            raise
