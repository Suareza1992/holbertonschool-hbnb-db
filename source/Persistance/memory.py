"""
This module exports a Repository that does not persist data,
it only stores it in memory.
"""

from datetime import datetime
import logging
from typing import Dict, Type, Optional
from src.models.base import Base
from src.persistence.repository import Repository
from utils.populate import populate_db

# Setup basic logging
logger = logging.getLogger(__name__)

class MemoryRepository(Repository):
    """
    A Repository that stores data in memory and does not persist it to disk.
    Data is lost every time the server is restarted.
    """

    def __init__(self) -> None:
        """Initialize the repository and populate it with initial data."""
        self.__data: Dict[str, Dict[str, Base]] = {
            "country": {},
            "user": {},
            "amenity": {},
            "city": {},
            "review": {},
            "place": {},
            "placeamenity": {},
        }
        self.reload()

    def get_all(self, model_name: str) -> list:
        """Return all objects of a given model."""
        return list(self.__data.get(model_name, {}).values())

    def get(self, model_name: str, obj_id: str) -> Optional[Base]:
        """Retrieve an object by its ID."""
        return self.__data.get(model_name, {}).get(obj_id)

    def reload(self) -> None:
        """Populates the repository with initial data."""
        try:
            populate_db(self)
            logger.info("Database populated successfully.")
        except Exception as e:
            logger.error(f"Failed to populate database: {e}")

    def save(self, obj: Base) -> None:
        """Save an object to the repository, ensuring no duplicate IDs."""
        cls = obj.__class__.__name__.lower()
        obj_dict = self.__data.setdefault(cls, {})
        if obj.id in obj_dict:
            logger.warning(f"Duplicate ID detected for {cls} with ID {obj.id}. Object not saved.")
            return
        obj_dict[obj.id] = obj
        logger.debug(f"Object saved: {cls} with ID {obj.id}")

    def update(self, obj: Base) -> Optional[Base]:
        """Update an existing object."""
        cls = obj.__class__.__name__.lower()
        obj_dict = self.__data.get(cls, {})
        if obj.id in obj_dict:
            obj.updated_at = datetime.now()
            obj_dict[obj.id] = obj
            logger.debug(f"Object updated: {cls} with ID {obj.id}")
            return obj
        logger.warning(f"Object not found for update: {cls} with ID {obj.id}")
        return None

    def delete(self, obj: Base) -> bool:
        """Remove an object from the repository."""
        cls = obj.__class__.__name__.lower()
        if obj.id in self.__data.get(cls, {}):
            del self.__data[cls][obj.id]
            logger.debug(f"Object deleted: {cls} with ID {obj.id}")
            return True
        logger.warning(f"Object not found for deletion: {cls} with ID {obj.id}")
        return False

