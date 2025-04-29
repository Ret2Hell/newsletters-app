from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import get_session
from app.models import (
    Newsletter,
    NewsletterCreate,
    NewsletterRead,
    NewsletterUpdate,
    PromptRequest,
)
from app.services.newsletter_generator import NewsletterGenerator

router = APIRouter(prefix="/newsletters", tags=["newsletters"])


@router.post("/generate/", status_code=status.HTTP_200_OK)
def generate_content(*, request: PromptRequest):
    ai_service = NewsletterGenerator()
    generated_content = ai_service.generate_content(request.prompt)
    return {"prompt": request.prompt, "generated_content": generated_content}


@router.post("/", response_model=NewsletterRead, status_code=status.HTTP_201_CREATED)
def create_newsletter(
    *, session: Session = Depends(get_session), newsletter: NewsletterCreate
):
    db_newsletter = Newsletter.model_validate(newsletter)
    session.add(db_newsletter)
    session.commit()
    session.refresh(db_newsletter)
    return db_newsletter


@router.get("/", response_model=List[NewsletterRead])
def get_newsletters(
    *, session: Session = Depends(get_session), skip: int = 0, limit: int = 10
):
    newsletters = session.exec(select(Newsletter).offset(skip).limit(limit)).all()
    return newsletters


@router.get("/{newsletter_id}", response_model=NewsletterRead)
def get_newsletter(*, session: Session = Depends(get_session), newsletter_id: UUID):
    newsletter = session.get(Newsletter, newsletter_id)
    if not newsletter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Newsletter not found"
        )
    return newsletter


@router.patch("/{newsletter_id}", response_model=NewsletterRead)
def update_newsletter(
    *,
    session: Session = Depends(get_session),
    newsletter_id: UUID,
    newsletter_update: NewsletterUpdate
):
    db_newsletter = session.get(Newsletter, newsletter_id)
    if not db_newsletter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Newsletter not found"
        )

    update_data = newsletter_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_newsletter, key, value)

    session.add(db_newsletter)
    session.commit()
    session.refresh(db_newsletter)
    return db_newsletter


@router.delete("/{newsletter_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_newsletter(*, session: Session = Depends(get_session), newsletter_id: UUID):
    newsletter = session.get(Newsletter, newsletter_id)
    if not newsletter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Newsletter not found"
        )

    session.delete(newsletter)
    session.commit()
    return None
