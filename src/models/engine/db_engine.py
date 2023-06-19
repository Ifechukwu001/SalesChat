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

classes = {"User": User, "UserBank": UserBank,
           "Product": Product, "OrderItem": OrderItem,
           "OrderDetail": OrderDetail, "CartItem": CartItem
           }


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
        if getenv("SC_ENV") == "test":
            Base.metadata.drop_all(self.__engine)
    
    def reload(self):
        """Loads the objects from the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session

    def close(self):
        """Closes the session"""
        if self.__session:
            self.__session.remove()

    def new(self, obj: any):
        """Adds a new object to the database
        Args:
            obj (any): Any Model instance
        """
        self.__session.add(obj)
        self.save()

    def save(self):
        """Saves the current session to the database"""
        self.__session.commit()

    def delete(self, obj: any):
        """Deletes an object from the session
        Args:
            obj (any): Any Model instance
        """
        self.__session.delete(obj)

    def all(self, cls: any = None) -> list[any]:
        """Returns all the objects of a session
        Args:
            cls (any): Class to query for.
        Returns:
            list(any): List of the objects of the class
        """
        if cls:
            if type(cls) == str:
                cls = classes.get(cls)
            if cls is not None:
                return self.__session.query(cls).all()
        objects = []
        for cls in classes.values():
            objs = self.__session.query(cls).all()
            objects.extend(objs)
        return objects

    def get(self, cls: any, id: str) -> any:
        """Returns an object of a session
        Args:
            cls (any): Class to query for.
            id (str): Id of the object.
        Returns:
            any: Object of a class
        """
        if type(cls) == str:
            cls = classes.get(cls)
        if cls is not None:
            return self.__session.query(cls).filter_by(id=id).first()
        
    def search(self, cls: any, *criterion, **fields) -> list[any]:
        """Searchs for an column in a class
        Args:
            cls (any): Class to query for
            fields: Kwargs to streamline the search
        Returns:
            list[any]: List of Objects found
        """
        if type(cls) == str:
            cls = classes.get(cls)
        if cls is not None:
            if criterion:
                return self.__session.query(cls).filter(*criterion).all()
            else:
                return self.__session.query(cls).filter_by(**fields).all()
