#!/usr/bin/env python3
"""Module containing the User model"""
from os import getenv
from dotenv import load_dotenv
from models.base import BaseModel, Base
from models.user_bank import UserBank
from models.product import Product
from models.cart_item import CartItem
from models.order_detail import OrderDetail
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import requests
import models

load_dotenv()
COUNTRY = "nigeria"


class User(BaseModel, Base):
    """User class"""

    if models.storage_type == "db":
        __tablename__ = "users"
        email = Column(String(60), unique=True)
        password = Column(String(60))
        phone = Column(String(45), unique=True)
        bank_id = Column(String(45), ForeignKey("user_banks.id"))
        products = relationship("Product")
        cart = relationship("CartItem")
        orders = relationship("OrderDetail")

    def __init__(self, email: str, password: str, phone: str):
        """Initializes the User object
        Args:
            email (str): User's email
            phone (str): User's password
        """
        super().__init__()
        self.email = email
        self.password = password
        self.phone = phone

    def update_bank_info(self, account_no: str,
                         bank_name: str, sort_code: str):
        """Updates the user bank information
        Args:
            account_no (str): Account Number of the user
            bank_name (str): Bank of the Account
            sort_code (str): Bank sort code
        """
        if self.bank_id is None:
            bank = UserBank(account_no, bank_name, sort_code)
            self.bank_id = bank.id
            self.update()
        else:
            bank = models.storage.get("UserBank", self.bank_id)
            bank.update(**{"account_no": account_no,
                           "bank_name": bank_name,
                           "sort_code": sort_code
                           })
        models.storage.save()

    def verify_bank(self, account_no: str, bank_name: str):
        """Checks if a bank account is valid
        Args:
            account_no (str): User Account Number
            bank_name (str): Bank name
        Returns:
            str: Bank name of the User
        """
        headers = {"Authorization": f"Bearer {getenv('SC_PAYSTACK_SECRET')}"}
        query = {"country": COUNTRY}
        bank_resp = requests.get("https://api.paystack.co/bank",
                                 params=query, headers=headers).json()
        bank_list = bank_resp["data"]
        user_bank = None
        for bank in bank_list:
            if bank_name.lower() in bank["name"].lower():
                user_bank = bank
        if user_bank:
            headers = {"Authorization":
                       f"Bearer {getenv('SC_PAYSTACK_SECRET')}"}
            query = {"account_number": account_no,
                     "bank_code": user_bank["code"]}
            user = requests.get("https://api.paystack.co/bank/resolve",
                                params=query, headers=headers).json()
            if user["status"]:
                self.update_bank_info(account_no, user_bank["name"],
                                      user_bank["code"])
                return {"status": True,
                        "message": "Bank information for "
                                   f"{user['data']['name']} has been updated"
                        }
            else:
                # Account number is incorrect
                return {"status": False,
                        "message": "The account number is incorrect"
                        }
        else:
            # The bank name is incorect
            return {"status": False,
                    "message": "The bank name is incorrect"
                    }

    def create_product(self, name: str, description: str,
                       price: int, quantity: int, category: str) -> Product:
        """Create a product of a user
        Args:
            name (str): Name of the product
            description (str): Description of the product
            price (int): Product's price
            quantity (int): Product's quantity
            category (str): product's category
        Returns:
            Product: Product object
        """
        product = Product(self.id, name, description, price,
                          quantity, category)
        self.products.append(product)
        return product

    def add_to_cart(self, product_id: str) -> CartItem:
        """Adds a product to cart
        Args:
            product_id (str): Product's ID
        Returns:
            CartItem: A cart item object
        """
        product = models.storage.get("Product", product_id)
        if product and product.is_available(1):
            cart_item = CartItem(1, product_id, self.id)
            self.cart.append(cart_item)
            return cart_item

    def checkout(self) -> str:
        """Checks out all carts item and process order
        Returns:
            str: Link for payment
        """
        order_detail = OrderDetail(self.id)
        amount = 0
        for item in self.cart:
            order_item = item.checkout(order_detail.id)
            order_detail.items.append(order_item)
            amount += order_item.total()
            item.delete()
        order_detail.total = amount

        if order_detail.total:
            headers = {"Authorization":
                       f"Bearer {getenv('SC_PAYSTACK_SECRET')}"}
            data = {"reference": order_detail.id,
                    "amount": order_detail.total * 100,
                    "callback_url": f"https://wa.me/{getenv('SC_CHAT_PHONE')}",
                    "email": self.email,
                    }
            resp = requests.post("https://api.paystack.co"
                                 "/transaction/initialize",
                                 headers=headers, json=data)
            resp_json = resp.json()
            if resp_json["status"]:
                self.orders.append(order_detail)
                return resp_json["data"]["authorization_url"]
            else:
                for item in order_detail.items:
                    item.delete()
                order_detail.delete()
        else:
            for item in order_detail.items:
                item.delete()
            order_detail.delete()
