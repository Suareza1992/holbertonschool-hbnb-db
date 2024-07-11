from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from datetime import datetime
import uuid
from abc import ABC, abstractmethod

Base = declarative_base()

class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Base(TimestampMixin, Base, ABC):
    __abstract__ = True

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self.__class__, key):
                setattr(self, key, value)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name not in ['created_at', 'updated_at']}

    @classmethod
    def get(cls, id):
        from src.persistence import repo
        return repo.get(cls, id)

    @classmethod
    def get_all(cls):
        from src.persistence import repo
        return repo.get_all(cls)

    @abstractmethod
    def save(self):
        raise NotImplementedError("Subclasses must implement save method.")

    @abstractmethod
    def delete(self):
        raise NotImplementedError("Subclasses must implement delete method.")

