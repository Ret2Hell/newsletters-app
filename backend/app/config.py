"""
Application configuration settings.

This module loads environment variables and provides a validated
settings object used throughout the application. Settings are loaded
from environment variables or .env files via python-dotenv.
"""

from dotenv import load_dotenv
from pydantic import field_validator
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """
    Application settings with validation.

    This class defines and validates all configuration settings required
    by the application. It uses Pydantic for automatic type conversion
    and validation of environment variables.

    Attributes:
        DATABASE_URL: Connection string for the SQLModel database
        GROQ_API_KEY: API key for accessing Groq AI services
        GROQ_MODEL: Model name to use for Groq AI completions (default: "gemma2-9b-it")
        TIMEZONE_OFFSET: Hours offset from UTC for datetime operations (default: 0)
    """

    DATABASE_URL: str
    GROQ_API_KEY: str
    GROQ_MODEL: str = "gemma2-9b-it"
    TIMEZONE_OFFSET: int = 0

    @field_validator("DATABASE_URL")
    def validate_database_url(cls, v):
        """
        Validate the database URL configuration.

        Args:
            v: The database URL value from environment

        Returns:
            str: The validated database URL

        Raises:
            ValueError: If the database URL is empty or not set
        """
        if not v:
            raise ValueError("DATABASE_URL must be set")
        return v

    @field_validator("GROQ_API_KEY")
    def validate_groq_api_key(cls, v):
        """
        Validate the Groq API key configuration.

        Args:
            v: The Groq API key value from environment

        Returns:
            str: The validated Groq API key

        Raises:
            ValueError: If the Groq API key is empty or not set
        """
        if not v:
            raise ValueError("GROQ_API_KEY must be set")
        return v


# Create a global settings instance for use throughout the application
settings = Settings()
