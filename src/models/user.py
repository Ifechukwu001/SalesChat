#!/usr/bin/env python3
"""Module containing the User model"""
import models
from models.base import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """User class"""

    if models.storage_type == "db":
        __tablename__ = "users"
        email = Column(String(60), unique=True)
        phone = Column(String(45), unique=True)
        bank_id = Column(String(45), ForeignKey("user_banks.id"))
        products = relationship("Product")
        cart = relationship("CartItem")
        orders = relationship("OrderDetail")

    def __init__(self, email: str, phone: str):
        """Initializes the User object
        Args:
            email (str): User's email
            phone (str): User's password
        """
        super().__init__()
        self.email = email
        self.phone = phone
