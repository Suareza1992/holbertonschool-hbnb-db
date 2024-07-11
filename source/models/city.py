# models.py
from datetime import datetime
from your_app import db
from src.models.country import Country
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class City(db.Model):
    """City representation"""

    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    country_code = db.Column(db.String(3), db.ForeignKey("countries.code"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    country = db.relationship('Country', back_populates='cities')
    places = db.relationship('Place', back_populates='city')

    def __init__(self, name: str, country_code: str, **kw):
        super().__init__(**kw)
        self.name = name
        self.country_code = country_code

    def __repr__(self):
        return f"<City {self.id} ({self.name})>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "country_code": self.country_code,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "City":
        """Create a new city"""
        country = Country.query.get(data["country_code"])
        if not country:
            raise ValueError("Country not found")

        city = City(**data)
        db.session.add(city)
        db.session.commit()
        return city

    @staticmethod
    def update(city_id: str, data: dict) -> "City | None":
        """Update an existing city"""
        city = City.query.get(city_id)
        if not city:
            raise ValueError("City not found")

        for key, value in data.items():
            setattr(city, key, value)

        db.session.commit()
        return city

    @staticmethod
    def get_all() -> list["City"]:
        return City.query.all()

    @staticmethod
    def get(city_id: str) -> "City | None":
        return City.query.get(city_id)

