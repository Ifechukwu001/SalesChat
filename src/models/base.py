#!/usr/bin/env python3
"""Module containing the Base Models
"""
from uuid import uuid4
from datetime import datetime
from models import storage_type
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

if storage_type == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel(Base):
    """BaseModel class"""

    if storage_type == "db":
        id = Column(String(45), default=str(uuid4()), primary_key=True)
        created_at = Column(DateTime, default=str(datetime.utcnow()))
        updated_at = Column(DateTime, default=str(datetime.utcnow()))

    def __init__(self):
        """Initializes the object"""
        self.id = str(uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def update(self, **kwargs: dict):
        """Updates the attribute of the object
        Args:
            kwargs (dict): Dictionary containing key-value pairs of attributes
        """
        for key, value in kwargs.items():
            if key == "created_at" or key == "updated_at":
                continue
            setattr(self, key, value)
        self.updated_at = datetime.utcnow()
