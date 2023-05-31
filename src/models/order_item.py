#!/usr/bin/env python3
"""Module containing OrderItem Module
"""
from models.base import BaseModel
from models import storage_type
from sqlalchemy import Column, String, Integer, ForeignKey


class OrderItem(BaseModel):
    """OrderItem class"""

    if storage_type == "db":
        __tablename__ = "order_items"
        quantity = Column(Integer)
        product_id = Column(String(45), ForeignKey("products.id"))
        user_id = Column(String(45), ForeignKey("users.id"))
        order_id = Column(String(45), ForeignKey("order_details.id"))

    def __init__(self, quantity: int, product_id: str,
                 user_id: str, order_id: str):
        """Initializes an OrderItem object
        Args:
            quantity (int): Product Quantity bought
            product_id (str): Product ID
            user_id (str): User ID
            order_id (str): Order ID
        """
        super().__init__()
        self.quantity = quantity
        self.product_id = product_id
        self.user_id = user_id
        self.order_id = order_id
