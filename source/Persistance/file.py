"""
This module exports a Repository that persists data in a JSON file.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from src.models.base import Base
from src.persistence.repository import Repository
from utils.constants import FILE_STORAGE_FILENAME

logger = logging.getLogger(__name__)

class FileRepository(Repository):
    """File Repository that manages data persistence in JSON format."""

    def __init__(self) -> None:
        """Initialize the FileRepository and load or populate data."""
        self.__filename = Path(FILE_STORAGE_FILENAME)
        self.__data = {}
        self.load_data()

    def load_data(self):
        """Load data from a file or initialize with default data."""
        if self.__filename.exists():
            with self.__filename.open('r') as file:
                file_data = json.load(file)
                self.deserialize_data(file_data)
        else:
            logger.info("Data file not found, initializing with default data.")
            self.__data = self.initialize_data()
            self.save_to_file()

    def save_to_file(self):
        """Save the serialized data to a JSON file."""
        with self.__filename.open('w') as file:
            json.dump(self.serialize_data(), file, indent=4)
        logger.debug("Data successfully saved to file.")

    def serialize_data(self):
        """Serialize the data for saving to JSON."""
        return {
            model: [obj.to_dict() for obj in objects]
            for model, objects in self.__data.items()
        }

    def deserialize_data(self, file_data):
        """Deserialize the JSON data into the repository data structure."""
        from src.models import Amenity, City, Country, Place, PlaceAmenity, Review, User
        model_classes = {
            'amenity': Amenity,
            'city': City,
            'country': Country,
            'place': Place,
            'placeamenity': PlaceAmenity,
            'review': Review,
            'user': User
        }
        for model, items in file_data.items():
            self.__data[model] = [model_classes[model](**item) for item in items]

    def get_all(self, model_name: str):
        """Return all objects of a given model."""
        return self.__data.get(model_name, [])

    def get(self, model_name: str, obj_id: str):
        """Get an object by its ID from the specified model collection."""
        for obj in self.get_all(model_name):
            if obj.id == obj_id:
                return obj
        return None

    def save(self, data: Base, save_to_file=True):
        """Add a new object to the repository and optionally save to file."""
        model = data.__class__.__name__.lower()
        self.__data.setdefault(model, []).append(data)
        if save_to_file:
            self.save_to_file()

    def update(self, obj: Base):
        """Update an existing object in the repository and save changes."""
        model = obj.__class__.__name__.lower()
        index = next((i for i, existing_obj in enumerate(self.__data[model]) if existing_obj.id == obj.id), None)
        if index is not None:
            self.__data[model][index] = obj
            self.save_to_file()
            return obj
        return None

    def delete(self, obj: Base):
        """Remove an object from the repository and save changes."""
        model = obj.__class__.__name__.lower()
        if obj in self.__data[model]:
            self.__data[model].remove(obj)
            self.save_to_file()
            return True
        return False

    def initialize_data(self):
        """Initialize default data structure."""
        return {
            "country": [],
            "user": [],
            "amenity": [],
            "city": [],
            "review": [],
            "place": [],
            "placeamenity": [],
        }


