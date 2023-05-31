#!/usr/bin/env python3
"""Module containing UserBank Model
"""
from models.base import BaseModel
from models import storage_type
from sqlalchemy import Column, String


class UserBank(BaseModel):
    """UserBank class"""

    if storage_type == "db":
        __tablename__ = "user_banks"
        account_no = Column(String(45))
        bank_name = Column(String(45))
        sort_code = Column(String(10))

    def __init__(self, account_no: str, bank_name: str, sort_code: str):
        """Initializes the UserBank object
        Args:
            account_no (str): User account number
            bank_name (str): User bank name
            sort_code (str): User bank sort code
        """
        super().__init__()
        self.account_no = account_no
        self.bank_name = bank_name
        self.sort_code = sort_code
