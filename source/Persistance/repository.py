from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional

# Define a type variable that can be any type.
T = TypeVar('T')

class Repository(ABC, Generic[T]):
    """
    Abstract class for a repository pattern that provides an interface for data access and manipulation.
    This pattern abstracts the data access layer, allowing different implementations based on the data source.

    Attributes:
        None

    Methods:
        reload: Reload or refresh data from the data source.
        get_all: Retrieve all objects of a specific type.
        get: Fetch a single object by its identifier.
        save: Save or persist an object in the data source.
        update: Update an existing object in the data source.
        delete: Remove an object from the data source.
    """

    @abstractmethod
    def reload(self) -> None:
        """
        Reload or refresh data from the data source.
        This method is typically used to initialize or synchronize the repository with the underlying data source.
        """
        pass

    @abstractmethod
    def get_all(self, model_name: str) -> List[T]:
        """
        Retrieve all objects of a specific type from the data source.

        Parameters:
            model_name (str): The name of the model type to retrieve.

        Returns:
            List[T]: A list of all objects of the specified model type.
        """
        pass

    @abstractmethod
    def get(self, model_name: str, id: str) -> Optional[T]:
        """
        Fetch a single object by its identifier.

        Parameters:
            model_name (str): The model type from which to retrieve the object.
            id (str): The unique identifier of the object to retrieve.

        Returns:
            Optional[T]: The object if found, otherwise None.
        """
        pass

    @abstractmethod
    def save(self, obj: T) -> None:
        """
        Save or persist an object in the data source.

        Parameters:
            obj (T): The object to save.
        """
        pass

    @abstractmethod
    def update(self, obj: T) -> None:
        """
        Update an existing object in the data source.

        Parameters:
            obj (T): The object to update.
        """
        pass

    @abstractmethod
    def delete(self, obj: T) -> bool:
        """
        Remove an object from the data source.

        Parameters:
            obj (T): The object to delete.

        Returns:
            bool: True if the object was successfully deleted, False otherwise.
        """
        pass

