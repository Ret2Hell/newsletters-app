from typing import List, Optional
from uuid import UUID

from app.models.newsletter import Newsletter, NewsletterCreate, NewsletterUpdate
from app.repositories.base import BaseRepository
from sqlmodel import Session


class NewsletterRepository(BaseRepository[Newsletter]):
    def __init__(self, session: Session):
        super().__init__(Newsletter, session)

    def create_newsletter(self, newsletter: NewsletterCreate) -> Newsletter:
        return self.create(newsletter)

    def get_newsletter(self, newsletter_id: UUID) -> Optional[Newsletter]:
        return self.get_by_id(newsletter_id)

    def get_newsletters(self, skip: int = 0, limit: int = 10) -> List[Newsletter]:
        return self.get_all(skip, limit)

    def update_newsletter(
        self, newsletter_id: UUID, newsletter: NewsletterUpdate
    ) -> Optional[Newsletter]:
        return self.update(newsletter_id, newsletter)

    def delete_newsletter(self, newsletter_id: UUID) -> bool:
        return self.delete(newsletter_id)
