import os
import logging

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Base configuration class with common settings
class Config:
    # Fallback if environment variable is not set
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'SQLALCHEMY_DATABASE_URI',
        'mysql://root:password@localhost/hbnb_default'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Add other SQLAlchemy configurations if necessary

# Development specific configuration
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DEV_DATABASE_URI',
        'mysql://root:password@localhost/hbnb_dev'
    )

# Testing specific configuration
class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'TEST_DATABASE_URI',
        'mysql://root:password@localhost/hbnb_test'
    )

# Production specific configuration
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'PROD_DATABASE_URI',
        'mysql://root:password@localhost/hbnb_prod'
    )
    # Ensure SSL is used for production database connections
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {
            "ssl": {
                "ca": "/path/to/ca-cert.pem",
                "cert": "/path/to/client-cert.pem",
                "key": "/path/to/client-key.pem"
            }
        }
    }

# Helper function to load the appropriate config based on the environment
def get_config():
    environment = os.getenv('FLASK_ENV', 'development')
    if environment == 'production':
        return ProductionConfig
    elif environment == 'testing':
        return TestingConfig
    else:
        return DevelopmentConfig

# Load the configuration
config = get_config()

# Validate configuration
if not config.SQLALCHEMY_DATABASE_URI:
    logger.error("SQLALCHEMY_DATABASE_URI cannot be empty.")
    raise ValueError("SQLALCHEMY_DATABASE_URI cannot be empty.")

logger.info(f"Loaded configuration for {os.getenv('FLASK_ENV', 'development')} environment.")

