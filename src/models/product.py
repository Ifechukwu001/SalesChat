#!/usr/bin/env python3
"""Module containing Product model
"""
import models
from models.base import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey


class Product(BaseModel, Base):
    """Product class"""

    if models.storage_type == "db":
        __tablename__ = "products"
        name = Column(String(45))
        description = Column(String(255), nullable=True)
        category = Column(String(45))
        price = Column(Integer)
        quantity = Column(Integer)
        seller_id = Column(String(45), ForeignKey("users.id"))

    def __init__(self, seller_id: str, name: str, description: str,
                 price: int, quantity: int, category: str):
        """Initializes the Product object
        Args:
            seller_id (str): User ID
            name (str): Product name
            description (str): Product description
            price (int): Product price
            quantity (int): Product Inventory
            category (str): Product Category
        """
        super().__init__()
        self.seller_id = seller_id
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        self.category = category
