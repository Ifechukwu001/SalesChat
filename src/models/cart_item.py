#!/usr/bin/env python3
"""Module containing Cart_item Model
"""
import models
from models.base import BaseModel, Base
from models.order_item import OrderItem
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

    def checkout(self, order_id: str) -> OrderItem:
        """Checks out itself into an orderitem
        Args:
            order_id (str): OrderDetail ID
        Returns:
            OrderItem: An instance of OrderItem
        """
        order_item = OrderItem(self.quantity, self.product_id, self.user_id, order_id)
        return order_item

    def total(self):
        """Gives the total price of the item
        Returns:
            int: Total amount
        """
        product = models.storage.get("Product", self.product_id)
        return product.price * self.quantity
