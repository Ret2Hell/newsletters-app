from typing import Generic, List, Optional, Type, TypeVar
from uuid import UUID

from sqlmodel import Session, SQLModel, select

T = TypeVar("T", bound=SQLModel)


class BaseRepository(Generic[T]):
    """
    Generic base repository for database operations.

    This class provides common CRUD operations that can be used
    with any SQLModel model. It's designed to be extended by
    specific repositories for each model type.

    Type Parameters:
        T: A SQLModel subclass that this repository will work with
    """

    def __init__(self, model_class: Type[T], session: Session):
        """
        Initialize the base repository.

        Args:
            model_class: The SQLModel class this repository will handle
            session: Database session for executing queries
        """
        self.model_class = model_class
        self.session = session

    def get_by_id(self, id: UUID) -> Optional[T]:
        """
        Retrieve a model instance by its ID.

        Args:
            id: UUID primary key of the model to retrieve

        Returns:
            Optional[T]: The model instance if found, None otherwise
        """
        return self.session.get(self.model_class, id)

    def get_all(self, skip: int = 0, limit: int = 10) -> List[T]:
        """
        Get a paginated list of model instances.

        Args:
            skip: Number of records to skip for pagination
            limit: Maximum number of records to return

        Returns:
            List[T]: List of model instances matching the pagination parameters
        """
        return self.session.exec(
            select(self.model_class).offset(skip).limit(limit)
        ).all()

    def create(self, obj_in: SQLModel) -> T:
        """
        Create a new model instance in the database.

        Args:
            obj_in: Input model data (typically a Pydantic model)

        Returns:
            T: The created model instance with database-generated fields
        """
        db_obj = self.model_class.model_validate(obj_in)
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def update(self, id: UUID, obj_in: SQLModel) -> Optional[T]:
        """
        Update an existing model instance.

        Only provided fields in obj_in will be updated (partial update).

        Args:
            id: UUID of the model instance to update
            obj_in: Input model with fields to update

        Returns:
            Optional[T]: The updated model instance if found, None otherwise
        """
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
        """
        Delete a model instance from the database.

        Args:
            id: UUID of the model instance to delete

        Returns:
            bool: True if the instance was found and deleted, False otherwise
        """
        db_obj = self.get_by_id(id)
        if not db_obj:
            return False

        self.session.delete(db_obj)
        self.session.commit()
        return True
