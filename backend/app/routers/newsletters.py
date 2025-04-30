from typing import List
from uuid import UUID

from app.database import get_session
from app.models import (
    Newsletter,
    NewsletterCreate,
    NewsletterRead,
    NewsletterUpdate,
    PromptRequest,
)
from app.services.newsletter_generator import NewsletterGenerator
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

router = APIRouter(prefix="/newsletters", tags=["newsletters"])


@router.post("/generate", status_code=status.HTTP_200_OK)
def generate_content(*, request: PromptRequest):
    try:
        ai_service = NewsletterGenerator()
        generated_content = ai_service.generate_content(request.prompt)
        return {"prompt": request.prompt, "generated_content": generated_content}
    except Exception as e:
        error_message = str(e)
        if "api_key" in error_message.lower():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Please check your API key.",
            )
        elif "rate limit" in error_message.lower():
            # Handle rate limiting
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please try again later.",
            )
        elif "timeout" in error_message.lower():
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Request timed out. Please try again later.",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate newsletter content: {error_message}",
            )


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
    newsletter_update: NewsletterUpdate,
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
