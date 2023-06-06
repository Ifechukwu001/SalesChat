#!/usr/bin/env python3
"""Module containing OrderDetail Model
"""
import models
from models.base import BaseModel, Base
from datetime import datetime
from sqlalchemy import Column, DateTime, Boolean, String, ForeignKey, Integer
from sqlalchemy.orm import relationship


class OrderDetail(BaseModel, Base):
    """OrderDetail class"""

    if models.storage_type == "db":
        __tablename__ = "order_details"
        initiated_date = Column(DateTime, default=str(datetime.utcnow()))
        payment_verified = Column(Boolean)
        product_delivered = Column(Boolean)
        total = Column(Integer, default=0)
        buyer_id = Column(String(45), ForeignKey("users.id"))
        items = relationship("OrderItem")

    def __init__(self, buyer_id: str):
        """Initializes the OrderDetail object
        Args:
            buyer_id (str): Buyer User ID
        """
        super().__init__()
        self.buyer_id = buyer_id
