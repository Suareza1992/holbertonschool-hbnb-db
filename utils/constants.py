import os
import logging

# Setting up basic logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Config:
    """
    Central configuration class for application settings.

    Attributes:
        REPOSITORY_ENV_VAR (str): Environment variable to determine the repository type.
        FILE_STORAGE_FILENAME (str): Filename for storing data in JSON format, configurable via environment.
        PICKLE_STORAGE_FILENAME (str): Filename for storing data using Pickle, configurable via environment.
    """
    REPOSITORY_ENV_VAR = "REPOSITORY"

    @staticmethod
    def get_env_variable(var_name, default):
        """ Retrieves environment variables safely with a default value. """
        value = os.getenv(var_name, default)
        if not value:
            logger.error(f"Environment variable {var_name} is not set; using default {default}.")
        else:
            logger.info(f"{var_name} set to {value}.")
        return value

    @staticmethod
    def validate_filename(filename):
        """ Validates file names to ensure they end with .json or .pkl """
        if not filename.endswith(('.json', '.pkl')):
            logger.error(f"Invalid file extension for {filename}.")
            raise ValueError("Storage filename must end with .json or .pkl")
        return filename

    # Environment variables can be set externally or default to 'data.json' and 'data.pkl'
    FILE_STORAGE_FILENAME = validate_filename(get_env_variable('FILE_STORAGE_FILENAME', 'data.json'))
    PICKLE_STORAGE_FILENAME = validate_filename(get_env_variable('PICKLE_STORAGE_FILENAME', 'data.pkl'))

def main():
    """ Main function to display current configuration. """
    logger.info(f"Using JSON storage file: {Config.FILE_STORAGE_FILENAME}")
    logger.info(f"Using Pickle storage file: {Config.PICKLE_STORAGE_FILENAME}")

if __name__ == "__main__":
    main()

