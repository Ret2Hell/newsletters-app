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

"""
Newsletter management endpoints.

This module contains all the API routes for creating, reading, updating,
and deleting newsletters, as well as generating newsletter content.
"""

router = APIRouter(prefix="/newsletters", tags=["newsletters"])


def get_newsletter_repository(
    session: Session = Depends(get_session),
) -> NewsletterRepository:
    """
    Dependency to get the newsletter repository.

    Args:
        session: Database session dependency

    Returns:
        NewsletterRepository: Repository for newsletter operations
    """
    return NewsletterRepository(session)


@router.post(
    "/generate", status_code=status.HTTP_200_OK, response_model=SuccessResponse
)
def generate_content(*, request: PromptRequest):
    """
    Generate newsletter content using AI.

    Args:
        request: PromptRequest object containing the prompt for content generation

    Returns:
        SuccessResponse: Contains the generated content and original prompt

    Raises:
        HTTPException: If content generation fails with various error codes depending on the error type
    """
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
    """
    Create a new newsletter.

    Args:
        newsletter: Newsletter data to create
        repo: Newsletter repository dependency

    Returns:
        SuccessResponse: Contains the created newsletter data
    """
    created = repo.create_newsletter(newsletter)
    return SuccessResponse(message="Newsletter created successfully", data=created)


@router.get("/", response_model=SuccessResponse[List[NewsletterRead]])
def get_newsletters(
    *,
    skip: int = 0,
    limit: int = 10,
    repo: NewsletterRepository = Depends(get_newsletter_repository),
):
    """
    Get a paginated list of newsletters.

    Args:
        skip: Number of records to skip for pagination
        limit: Maximum number of records to return
        repo: Newsletter repository dependency

    Returns:
        SuccessResponse: Contains a list of newsletters
    """
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
    """
    Get a specific newsletter by ID.

    Args:
        newsletter_id: UUID of the newsletter to retrieve
        repo: Newsletter repository dependency

    Returns:
        SuccessResponse: Contains the requested newsletter data

    Raises:
        HTTPException: 404 if newsletter not found
    """
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
    """
    Update a newsletter.

    Args:
        newsletter_id: UUID of the newsletter to update
        newsletter_update: Data to update in the newsletter
        repo: Newsletter repository dependency

    Returns:
        SuccessResponse: Contains the updated newsletter data

    Raises:
        HTTPException: 404 if newsletter not found
    """
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
    """
    Delete a newsletter.

    Args:
        newsletter_id: UUID of the newsletter to delete
        repo: Newsletter repository dependency

    Returns:
        SuccessResponse: Contains empty data on successful deletion

    Raises:
        HTTPException: 404 if newsletter not found
    """
    if not repo.delete_newsletter(newsletter_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Newsletter not found"
        )
    return SuccessResponse(message="Newsletter deleted successfully", data={})
