#!/usr/bin/env python3
"""Module containing OrderDetail Model
"""
from models.base import BaseModel
from models import storage_type
from datetime import datetime
from sqlalchemy import Column, DateTime, Boolean, String, ForeignKey


class OrderDetail(BaseModel):
    """OrderDetail class"""

    if storage_type == "db":
        __tablename__ = "order_details"
        initiated_date = Column(DateTime, default=str(datetime.utcnow()))
        payment_verified = Column(Boolean)
        product_delivered = Column(Boolean)
        buyer_id = Column(String(45), ForeignKey("users.id"))

    def __init__(self, buyer_id: str):
        """Initializes the OrderDetail object
        Args:
            buyer_id (str): Buyer User ID
        """
        super().__init__()
        self.buyer_id = buyer_id
