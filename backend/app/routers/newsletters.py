from typing import List
from uuid import UUID

from app.database import get_session
from app.models.newsletter import (
    NewsletterCreate,
    NewsletterRead,
    NewsletterUpdate,
    PromptRequest,
)
from app.models.response import SuccessResponse
from app.repositories.newsletter import NewsletterRepository
from app.services.newsletter_generator import NewsletterGenerator
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

router = APIRouter(prefix="/newsletters", tags=["newsletters"])


def get_newsletter_repository(
    session: Session = Depends(get_session),
) -> NewsletterRepository:
    return NewsletterRepository(session)


@router.post(
    "/generate", status_code=status.HTTP_200_OK, response_model=SuccessResponse
)
def generate_content(*, request: PromptRequest):
    try:
        ai_service = NewsletterGenerator()
        generated_content = ai_service.generate_content(request.prompt)
        return SuccessResponse(
            message="Content generated successfully",
            data={"prompt": request.prompt, "generated_content": generated_content},
        )
    except Exception as e:
        error_message = str(e)
        if "api_key" in error_message.lower():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Please check your API key.",
            )
        elif "rate limit" in error_message.lower():
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


@router.post(
    "/",
    response_model=SuccessResponse[NewsletterRead],
    status_code=status.HTTP_201_CREATED,
)
def create_newsletter(
    *,
    newsletter: NewsletterCreate,
    repo: NewsletterRepository = Depends(get_newsletter_repository),
):
    created = repo.create_newsletter(newsletter)
    return SuccessResponse(message="Newsletter created successfully", data=created)


@router.get("/", response_model=SuccessResponse[List[NewsletterRead]])
def get_newsletters(
    *,
    skip: int = 0,
    limit: int = 10,
    repo: NewsletterRepository = Depends(get_newsletter_repository),
):
    newsletters = repo.get_newsletters(skip, limit)
    return SuccessResponse(
        message="Newsletters retrieved successfully", data=newsletters
    )


@router.get("/{newsletter_id}", response_model=SuccessResponse[NewsletterRead])
def get_newsletter(
    *,
    newsletter_id: UUID,
    repo: NewsletterRepository = Depends(get_newsletter_repository),
):
    newsletter = repo.get_newsletter(newsletter_id)
    if not newsletter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Newsletter not found"
        )
    return SuccessResponse(message="Newsletter retrieved successfully", data=newsletter)


@router.patch("/{newsletter_id}", response_model=SuccessResponse[NewsletterRead])
def update_newsletter(
    *,
    newsletter_id: UUID,
    newsletter_update: NewsletterUpdate,
    repo: NewsletterRepository = Depends(get_newsletter_repository),
):
    newsletter = repo.update_newsletter(newsletter_id, newsletter_update)
    if not newsletter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Newsletter not found"
        )
    return SuccessResponse(message="Newsletter updated successfully", data=newsletter)


@router.delete(
    "/{newsletter_id}", status_code=status.HTTP_200_OK, response_model=SuccessResponse
)
def delete_newsletter(
    *,
    newsletter_id: UUID,
    repo: NewsletterRepository = Depends(get_newsletter_repository),
):
    if not repo.delete_newsletter(newsletter_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Newsletter not found"
        )
    return SuccessResponse(message="Newsletter deleted successfully", data={})
