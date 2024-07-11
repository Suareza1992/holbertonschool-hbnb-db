# models.py
from datetime import datetime
from your_app import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    first_name = db.Column(db.String(36), nullable=False)
    last_name = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    places = db.relationship("Place", back_populates='host')
    reviews = db.relationship("Review", back_populates='user')

    def __init__(self, email: str, password: str, is_admin: bool, first_name: str, last_name: str, **kw):
        super().__init__(**kw)
        self.email = email
        self.set_password(password)
        self.is_admin = is_admin
        self.first_name = first_name
        self.last_name = last_name

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.id} ({self.email})>"

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'is_admin': self.is_admin,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @staticmethod
    def create(user_data: dict) -> "User":
        from src.persistence import repo

        users = User.get_all()

        for u in users:
            if u.email == user_data["email"]:
                raise ValueError("User already exists")

        new_user = User(**user_data)
        repo.save(new_user)
        return new_user

    @staticmethod
    def update(user_id: str, data: dict) -> "User | None":
        from src.persistence import repo

        user = User.query.get(user_id)

        if not user:
            return None

        if "email" in data:
            user.email = data["email"]
        if "password" in data:
            user.set_password(data["password"])
        if "is_admin" in data:
            user.is_admin = data["is_admin"]
        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]

        repo.update(user)
        return user

    @staticmethod
    def get_all() -> list["User"]:
        return User.query.all()

    @staticmethod
    def get(user_id: str) -> "User | None":
        return User.query.get(user_id)

