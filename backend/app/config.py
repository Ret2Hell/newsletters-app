from dotenv import load_dotenv
from pydantic import field_validator
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str
    GROQ_API_KEY: str
    GROQ_MODEL: str = "gemma2-9b-it"
    TIMEZONE_OFFSET: int = 0

    @field_validator("DATABASE_URL")
    def validate_database_url(cls, v):
        if not v:
            raise ValueError("DATABASE_URL must be set")
        return v

    @field_validator("GROQ_API_KEY")
    def validate_groq_api_key(cls, v):
        if not v:
            raise ValueError("GROQ_API_KEY must be set")
        return v


settings = Settings()
