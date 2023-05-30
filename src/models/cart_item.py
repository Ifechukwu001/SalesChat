#!/usr/bin/env python3
"""Module containing Cart_item Model
"""
from models.base import BaseModel


class CartItem(BaseModel):
    """CartItem class"""

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
