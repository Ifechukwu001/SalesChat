#!/usr/bin/env python3
"""Module containing Cart_item Model
"""
import models
from models.base import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey


class CartItem(BaseModel, Base):
    """CartItem class"""

    if models.storage_type == "db":
        __tablename__ = "cart_items"
        quantity = Column(Integer)
        product_id = Column(String(45), ForeignKey("products.id"))
        user_id = Column(String(45), ForeignKey("users.id"))

    def __init__(self, quantity: int, product_id: str, user_id: str):
        """Initializes the CartItem object
        Args:
            quantity (int): Quantity to be bought
            product_id (str): Product ID
            user_id (str): User ID
        """
        super().__init__()
        self.quantity = quantity
        self.product_id = product_id
        self.user_id = user_id
