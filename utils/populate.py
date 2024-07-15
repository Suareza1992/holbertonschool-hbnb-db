import logging
from src.persistence.repository import Repository
import pycountry
from src.models.country import Country

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def populate_db(repo: Repository, data_set='countries') -> None:
    """
    Populates the database with specified data set from pycountry.

    Parameters:
    repo: Repository - Repository object capable of database transactions.
    data_set: str - Specific data set to populate ('countries', 'languages', etc.).
    """
    try:
        if data_set == 'countries':
            populate_countries(repo)
        # Additional data sets can be handled here
        logger.info("Database successfully populated with %s", data_set)
    except Exception as e:
        logger.error("Failed to populate the database: %s", e)

def populate_countries(repo: Repository):
    """
    Populates the database with country data using batch insertion to improve performance.

    Parameters:
    repo: Repository - Repository object capable of database transactions.
    """
    new_countries = []
    for c in pycountry.countries:
        if repo.get_by_code(Country, c.alpha_2) is None:
            new_countries.append(Country(c.name, c.alpha_2))

    if new_countries:
        repo.save_all(new_countries)  # Assuming 'save_all' is a batch operation method in the repository
        logger.info("Added %d new countries to the database.", len(new_countries))

if __name__ == "__main__":
    # Example usage
    from your_repository_implementation import YourRepository  # Replace with your actual repository import
    repo = YourRepository()
    populate_db(repo, 'countries')

