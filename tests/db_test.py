import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.persistence.db import DBRepository
from src.models.base import Base
from src.models.user import User
from src.models.amenity import Amenity
from src.models.review import Review
from src.models.place import Place
from src.models.city import City
from src.models.country import Country
from parameterized import parameterized

class TestDatabaseCRUD(unittest.TestCase):
    def setUp(self):
        # Setup an in-memory SQLite database for testing
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.DBSession = sessionmaker(bind=self.engine)
        self.session = self.DBSession()
        self.db_repository = DBRepository(engine=self.engine, db_session=self.session)

    @parameterized.expand([
        (User, {"first_name": "Test", "last_name": "User", "email": "testuser@example.com"}),
        (City, {"name": "TestCity"}),
        (Country, {"name": "TestCountry", "code": "TC"}),
        # Additional models can be tested here
    ])
    def test_create_entity(self, model, kwargs):
        entity = self.db_repository.create(model, **kwargs)
        self.session.commit()
        # Assert that the entity is not None and check specific attributes
        self.assertIsNotNone(entity.id)
        for key, value in kwargs.items():
            self.assertEqual(getattr(entity, key), value, f"{key} does not match in {model.__name__}")

    def tearDown(self):
        # Drop all the metadata
        Base.metadata.drop_all(self.engine)

if __name__ == "__main__":
    unittest.main()

