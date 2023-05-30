#!/usr/bin/env python3
"""Module containing the User model"""
from models.base import BaseModel


class User(BaseModel):

    def __init__(self, email: str, phone: str):
        """Initializes the User object
        Args:
            email (str): User's email
            phone (str): User's password
        """
        super().__init__()
        self.email = email
        self.phone = phone
