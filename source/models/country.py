# models.py
from your_app import db

class Country(db.Model):
    __tablename__ = 'countries'

    name = db.Column(db.String(128), unique=True, nullable=False)
    code = db.Column(db.String(3), unique=True, primary_key=True, nullable=False)
    cities = db.relationship("City", back_populates='country')

    def __init__(self, name: str, code: str, **kw):
        super().__init__(**kw)
        self.name = name
        self.code = code

    def __repr__(self):
        return f"<Country {self.code} ({self.name})>"

    def to_dict(self):
        return {
            "name": self.name,
            "code": self.code,
        }

    @staticmethod
    def get_all():
        from your_app.data_manager import data_manager
        return data_manager.get_all_countries()

    @staticmethod
    def get(code: str):
        from your_app.data_manager import data_manager
        return data_manager.get_country(code)

    @staticmethod
    def create(name: str, code: str):
        from your_app.data_manager import data_manager
        return data_manager.create_country(name, code)

