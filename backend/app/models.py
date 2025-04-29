from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel
from sqlmodel import Field, SQLModel

from app.utils import get_utc_now


class NewsletterBase(SQLModel):
    prompt: str
    generated_content: str
    edited_content: str


class Newsletter(NewsletterBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=get_utc_now)
    updated_at: datetime = Field(
        default_factory=get_utc_now, sa_column_kwargs={"onupdate": get_utc_now}
    )


class NewsletterCreate(NewsletterBase):
    pass


class NewsletterRead(NewsletterBase):
    id: UUID
    created_at: datetime
    updated_at: datetime


class NewsletterUpdate(SQLModel):
    edited_content: Optional[str] = None


class PromptRequest(BaseModel):
    prompt: str
