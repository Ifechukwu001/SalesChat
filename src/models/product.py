#!/usr/bin/env python3
"""Module containing Product model
"""
from models.base import BaseModel


class Product(BaseModel):
    """Product class"""

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
