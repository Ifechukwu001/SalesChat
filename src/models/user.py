#!/usr/bin/env python3
"""Module containing the User model"""
from models.base import BaseModel
from models import storage_type
from sqlalchemy import Column, String, ForeignKey


class User(BaseModel):
    """User class"""

    if storage_type == "db":
        __tablename__ = "users"
        email = Column(String(60), unique=True)
        phone = Column(String(45), unique=True)
        bank_id = Column(String(45), ForeignKey("user_banks.id"),
                         nullable=True)

    def __init__(self, email: str, phone: str):
        """Initializes the User object
        Args:
            email (str): User's email
            phone (str): User's password
        """
        super().__init__()
        self.email = email
        self.phone = phone
