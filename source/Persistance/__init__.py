"""
This module is responsible for selecting the repository to be used based on the
environment variable REPOSITORY_ENV_VAR.
"""

import os
import logging
from src.persistence.repository import Repository
from utils.constants import REPOSITORY_ENV_VAR

# Set up logging
logger = logging.getLogger(__name__)

def get_repository() -> Repository:
    """Factory function to get the appropriate repository based on the environment setting."""
    repo_type = os.getenv(REPOSITORY_ENV_VAR, 'memory')  # Default to 'memory' if unset
    logger.debug(f"Selected repository type: {repo_type}")

    try:
        if repo_type == "db":
            from src.persistence.db import DBRepository
            return DBRepository()
        elif repo_type == "file":
            from src.persistence.file import FileRepository
            return FileRepository()
        elif repo_type == "pickle":
            from src.persistence.pickled import PickleRepository
            return PickleRepository()
        else:
            from src.persistence.memory import MemoryRepository
            return MemoryRepository()
    except ImportError as e:
        error_msg = f"Repository type '{repo_type}' is not implemented: {str(e)}"
        logger.error(error_msg)
        raise ImportError(error_msg)

# Repository instance for use throughout the application
repo = get_repository()
logger.info(f"Using {repo.__class__.__name__} as repository")

