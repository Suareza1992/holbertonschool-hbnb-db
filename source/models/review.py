# models.py
from datetime import datetime
from your_app import db
from src.models.place import Place
from src.models.user import User
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    place = db.relationship("Place", back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')

    def __init__(self, place_id: str, user_id: str, comment: str, rating: float, **kw):
        super().__init__(**kw)
        self.place_id = place_id
        self.user_id = user_id
        self.comment = comment
        self.rating = rating

    def __repr__(self) -> str:
        return f"<Review {self.id} - '{self.comment[:25]}...'>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "place_id": self.place_id,
            "user_id": self.user_id,
            "comment": self.comment,
            "rating": self.rating,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "Review":
        from src.persistence import repo

        user = User.query.get(data["user_id"])
        if not user:
            raise ValueError(f"User with ID {data['user_id']} not found")

        place = Place.query.get(data["place_id"])
        if not place:
            raise ValueError(f"Place with ID {data['place_id']} not found")

        new_review = Review(**data)
        repo.save(new_review)
        return new_review

    @staticmethod
    def update(review_id: str, data: dict) -> "Review | None":
        from src.persistence import repo

        review = Review.query.get(review_id)
        if not review:
            raise ValueError("Review not found")

        for key, value in data.items():
            setattr(review, key, value)

        repo.update(review)
        return review

    @staticmethod
    def get_all() -> list["Review"]:
        return Review.query.all()

    @staticmethod
    def get(review_id: str) -> "Review | None":
        return Review.query.get(review_id)

