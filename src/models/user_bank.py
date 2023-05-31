#!/usr/bin/env python3
"""Module containing UserBank Model
"""
from models.base import BaseModel


class UserBank(BaseModel):
    """UserBank class"""

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
