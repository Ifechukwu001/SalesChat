#!/usr/bin/env python3
"""Module containing DB Engine
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base import Base
from models.cart_item import CartItem
from models.order_detail import OrderDetail
from models.order_item import OrderItem
from models.product import Product
from models.user import User
from models.user_bank import UserBank
from os import getenv


class DBEngine:
    """DBEngine class"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes and creates a connection to the database"""
        SC_USER = getenv("SC_USER")
        SC_PASS = getenv("SC_PASS")
        SC_HOST = getenv("SC_HOST")
        SC_DB = getenv("SC_DB")
        self.__engine = create_engine(f"mysql+mysqldb://{SC_USER}:{SC_PASS}"
                                      f"@{SC_HOST}/{SC_DB}")
    
    def reload(self):
        """Loads the objects from the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session

    def new(self, obj: any):
        """Adds a new object to the database
        Args:
            obj (any): Any Model instance
        """
        self.__session.add(obj)

    def save(self):
        """Saves the current session to the database"""
        self.__session.commit()

    def delete(self, obj: any):
        """Deletes an object from the session
        Args:
            obj (any): Any Model instance
        """
        self.__session.delete(obj)
