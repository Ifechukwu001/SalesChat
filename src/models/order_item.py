#!/usr/bin/env python3
"""Module containing OrderItem Module
"""
from models.base import BaseModel


class OrderItem(BaseModel):
    """OrderItem class"""

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
