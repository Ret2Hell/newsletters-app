from typing import Generic, List, Optional, Type, TypeVar
from uuid import UUID

from sqlmodel import Session, SQLModel, select

T = TypeVar("T", bound=SQLModel)


class BaseRepository(Generic[T]):
    def __init__(self, model_class: Type[T], session: Session):
        self.model_class = model_class
        self.session = session

    def get_by_id(self, id: UUID) -> Optional[T]:
        return self.session.get(self.model_class, id)

    def get_all(self, skip: int = 0, limit: int = 10) -> List[T]:
        return self.session.exec(
            select(self.model_class).offset(skip).limit(limit)
        ).all()

    def create(self, obj_in: SQLModel) -> T:
        db_obj = self.model_class.model_validate(obj_in)
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def update(self, id: UUID, obj_in: SQLModel) -> Optional[T]:
        db_obj = self.get_by_id(id)
        if not db_obj:
            return None

        update_data = obj_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_obj, key, value)

        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def delete(self, id: UUID) -> bool:
        db_obj = self.get_by_id(id)
        if not db_obj:
            return False

        self.session.delete(db_obj)
        self.session.commit()
        return True
