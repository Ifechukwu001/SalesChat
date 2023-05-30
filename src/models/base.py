#!/usr/bin/env python3
"""Module containing the Base Models
"""
from uuid import uuid4
from datetime import datetime


class BaseModel:

    def __init__(self):
        """Initializes the object"""
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def update(self, **kwargs: dict):
        """Updates the attribute of the object
        Args:
            kwargs (dict): Dictionary containing key-value pairs of attributes
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.updated_at = datetime.now()
