from typing import List, Optional
from uuid import UUID

from app.models.newsletter import Newsletter, NewsletterCreate, NewsletterUpdate
from app.repositories.base import BaseRepository
from sqlmodel import Session


class NewsletterRepository(BaseRepository[Newsletter]):
    """
    Repository for handling newsletter database operations.

    This class extends the BaseRepository with Newsletter-specific functionality,
    providing methods to create, read, update, and delete Newsletter objects.
    """

    def __init__(self, session: Session):
        """
        Initialize the NewsletterRepository.

        Args:
            session: SQLModel database session
        """
        super().__init__(Newsletter, session)

    def create_newsletter(self, newsletter: NewsletterCreate) -> Newsletter:
        """
        Create a new newsletter in the database.

        Args:
            newsletter: Newsletter creation model with required fields

        Returns:
            Newsletter: The created newsletter with generated ID
        """
        return self.create(newsletter)

    def get_newsletter(self, newsletter_id: UUID) -> Optional[Newsletter]:
        """
        Retrieve a newsletter by its ID.

        Args:
            newsletter_id: UUID of the newsletter to retrieve

        Returns:
            Optional[Newsletter]: The newsletter if found, None otherwise
        """
        return self.get_by_id(newsletter_id)

    def get_newsletters(self, skip: int = 0, limit: int = 10) -> List[Newsletter]:
        """
        Get a paginated list of newsletters.

        Args:
            skip: Number of records to skip for pagination
            limit: Maximum number of records to return

        Returns:
            List[Newsletter]: List of newsletters matching the pagination parameters
        """
        return self.get_all(skip, limit)

    def update_newsletter(
        self, newsletter_id: UUID, newsletter: NewsletterUpdate
    ) -> Optional[Newsletter]:
        """
        Update an existing newsletter.

        Args:
            newsletter_id: UUID of the newsletter to update
            newsletter: Newsletter update model with fields to update

        Returns:
            Optional[Newsletter]: The updated newsletter if found, None otherwise
        """
        return self.update(newsletter_id, newsletter)

    def delete_newsletter(self, newsletter_id: UUID) -> bool:
        """
        Delete a newsletter from the database.

        Args:
            newsletter_id: UUID of the newsletter to delete

        Returns:
            bool: True if the newsletter was found and deleted, False otherwise
        """
        return self.delete(newsletter_id)
