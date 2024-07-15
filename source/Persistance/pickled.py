"""
This module exports a Repository that persists data in a pickle file.
"""

import pickle
import logging
from src.persistence.repository import Repository
from utils.constants import PICKLE_STORAGE_FILENAME

logger = logging.getLogger(__name__)

class PickleRepository(Repository):
    """Pickle Repository for more secure and optimized data handling."""

    def __init__(self) -> None:
        """Initialize the repository and load or populate data."""
        self.__filename = PICKLE_STORAGE_FILENAME
        self.__data = {}
        self.load_data()

    def load_data(self):
        """Load data from a pickle file or initialize with default data if the file does not exist."""
        try:
            with open(self.__filename, 'rb') as file:
                self.__data = pickle.load(file, fix_imports=False)
            logger.info("Data loaded successfully from the pickle file.")
        except FileNotFoundError:
            logger.warning("Pickle file not found, initializing with default data.")
            self.__data = self.initialize_data()
            self.save_data()
        except pickle.PickleError as e:
            logger.error(f"Failed to load data due to pickle error: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred during data loading: {e}")

    def save_data(self):
        """Save the serialized data to a pickle file securely."""
        try:
            with open(self.__filename, 'wb') as file:
                pickle.dump(self.__data, file, protocol=pickle.HIGHEST_PROTOCOL)
            logger.info("Data saved successfully to the pickle file.")
        except pickle.PickleError as e:
            logger.error(f"Failed to save data due to pickle error: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred during data saving: {e}")

    def get_all(self, model_name: str) -> list:
        """Return all objects of a given model from the memory."""
        return self.__data.get(model_name, [])

    def get(self, model_name: str, obj_id: str):
        """Retrieve an object by its ID from the stored data."""
        for obj in self.get_all(model_name):
            if obj.id == obj_id:
                return obj
        return None

    def save(self, obj, save_to_file=True):
        """Add a new object to the repository and optionally save to file."""
        model = obj.__class__.__name__.lower()
        self.__data.setdefault(model, []).append(obj)
        if save_to_file:
            self.save_data()

    def update(self, obj):
        """Update an existing object in the repository and save changes."""
        model = obj.__class__.__name__.lower()
        for i, existing_obj in enumerate(self.__data[model]):
            if existing_obj.id == obj.id:
                self.__data[model][i] = obj
                self.save_data()
                return

    def delete(self, obj) -> bool:
        """Remove an object from the repository and update the file."""
        model = obj.__class__.__name__.lower()
        if obj in self.__data[model]:
            self.__data[model].remove(obj)
            self.save_data()
            return True
        return False

    def initialize_data(self):
        """Initialize default data structure if the file is not found."""
        return {
            "country": [],
            "user": [],
            "amenity": [],
            "city": [],
            "review": [],
            "place": [],
            "placeamenity": [],
        }

