"""
This module is responsible for selecting the repository to be used based on the
environment variable REPOSITORY_ENV_VAR.
"""

import os
import logging
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, NoResultFound
from src.models.base import Base
from src.persistence.repository import Repository
from src.models import db

# Set up logging
logger = logging.getLogger(__name__)

class DBRepository(Repository):
    """A database repository implementing the Repository interface for SQLAlchemy ORM."""

    def __init__(self) -> None:
        """Initialize the DBRepository with a database session."""
        self.session = db.session
        self.reload()

    def get_all(self, model_name: str) -> list:
        """Retrieve all objects of a given model from the database."""
        try:
            return self.session.query(model_name).all()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching all objects for {model_name}: {str(e)}")
            self.session.rollback()
            return []

    def get(self, model_name: str, obj_id: str) -> Base | None:
        """Retrieve an object of a given model by its ID from the database."""
        try:
            return self.session.query(model_name).get(obj_id)
        except NoResultFound:
            logger.info(f"No result found for {model_name} with ID {obj_id}")
            return None
        except IntegrityError as e:
            logger.error(f"Integrity error while accessing {model_name}: {str(e)}")
            self.session.rollback()
            return None

    def reload(self) -> None:
        """Optionally repopulate the database with initial data."""
        try:
            db.create_all()
            from utils.populate import populate_db
            populate_db(self)
        except SQLAlchemyError as e:
            logger.error(f"Failed to reload database: {str(e)}")

    def save(self, obj: Base) -> None:
        """Save an object to the database."""
        try:
            self.session.add(obj)
            self.session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Failed to save object: {str(e)}")
            self.session.rollback()

    def update(self, obj: Base) -> Base | None:
        """Commit changes to the database to update an object."""
        try:
            self.session.commit()
            return obj
        except SQLAlchemyError as e:
            logger.error(f"Failed to update object {obj.id}: {str(e)}")
            self.session.rollback()
            return None

    def delete(self, obj: Base) -> bool:
        """Delete an object from the database."""
        try:
            self.session.delete(obj)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            logger.error(f"Failed to delete object {obj.id}: {str(e)}")
            self.session.rollback()
            return False

    def get_by_code(self, model, code):
        """Retrieve an object by its unique code."""
        try:
            return self.session.query(model).filter(model.code == code).first()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving object by code {code}: {str(e)}")
            self.session.rollback()
            return None


