#!/usr/bin/env python3
"""WhatsApp Model
"""
import models
from models.user import User
import requests
from os import getenv


class WhatsAppSender:
    """WhatsAppSender class"""
    authorisation = getenv("WHATSAPP_TOKEN")

    @classmethod
    def process(cls, information: dict):
        """Processes the information and responds appropiately"""
        if information["field"] == "messages":
            message = information["value"].get("messages")
            if message:
                phone_number = message[0]["from"]
                message_type = message[0]["type"]


                if message_type == "text":
                    body = message[0]["text"]["body"]
                    if body.lower().startswith("hello"):
                        WhatsAppSender.hello(phone_number)
                        WhatsAppSender.options(phone_number)
                    elif body.lower().startswith("sell"):
                        WhatsAppSender.sell(phone_number)
                    elif body.lower().startswith("register"):
                        WhatsAppSender.register(phone_number)
                    elif body.lower().startswith("user"):
                        WhatsAppSender.create_user(body, phone_number)
                    elif body.lower().startswith("bank"):
                        WhatsAppSender.bank_details(phone_number)
                    elif body.lower().startswith("update"):
                        WhatsAppSender.update_user(body, phone_number)
                    
    @classmethod
    def hello(cls, phone_number: str):
        """Sends hello to the phone number
        Args:
            phone_number (str): Phone number to send the message.
        """
        message = "*Welcome to SalesChat*\n" \
                  "_No 1 WhatsApp Marketplace_"
        
        WhatsAppSender.message(message, phone_number)

    @classmethod
    def options(cls, phone_number: str):
        """Sends Options to the phone number
        Args:
            phone_number (str): Phone number to send the message.
        """
        message = "Send a corresponding prompt:\n\n" \
                  "*sell*: To sell a product\n" \
                  "*add*: Add to cart\n"
        
        WhatsAppSender.message(message, phone_number)

    @classmethod
    def sell(cls, phone_number: str):
        """Sends Sell template to the phone number
        Args:
            phone_number (str): Phone number to send the message.
        """
        users = models.storage.search("User", phone=phone_number)
        if users:
            user = users[0]
            if user.bank_id:
                msg = "Send the product information " \
                      "using this template (Copy the template and edit)\n\n"
                WhatsAppSender.message(msg, phone_number)
                msg = "product\n" \
                      "name: \n" \
                      "description: \n" \
                      "price: \n" \
                      "category: (good/service/digital)\n"\
                      "quantity: "
                WhatsAppSender.message(msg, phone_number)
                msg = "Ps: Leave quantity blank if product " \
                      "is digital. Select only one category"
                WhatsAppSender.message(msg, phone_number)
                
            else:
                msg = "You have not added your bank details\n" \
                      "Prompt - *bank*"
                WhatsAppSender.message(msg, phone_number)
        else:
            msg = "You have not been registered.\n" \
                  "Prompt - *register*"
            WhatsAppSender.message(msg, phone_number)

    @classmethod
    def register(cls, phone_number: str):
        """Sends register template to the phone number
        Args:
            phone_number (str): Phone number to send the message
        """
        msg = "Send the product information " \
              "using this template (Copy the template and edit)\n\n"
        WhatsAppSender.message(msg, phone_number)

        msg = "user\n" \
              "email: \n" \
              "password: "
        WhatsAppSender.message(msg, phone_number)

        msg = "PS: To ensure privacy, " \
              "delete your message after sending"
        WhatsAppSender.message(msg, phone_number)

    @classmethod
    def bank_details(cls, phone_number: str):
        """Sends bank details template to the phone number
        Args:
            phone_number (str): Phone number to send the message
        """
        msg = "Send your bank information " \
              "using this template (Copy the template and edit)\n\n"
        WhatsAppSender.message(msg, phone_number)

        msg = "update\n" \
              "email: \n" \
              "account number: \n" \
              "bank name: \n" \
              "bank sort code: \n" \
              "password: "
        WhatsAppSender.message(msg, phone_number)

        msg = "PS: To ensure privacy, " \
              "delete your message after sending. \n" \
              "You can change everything, except your password, " \
              "that must be the old one."
        WhatsAppSender.message(msg, phone_number)

    @classmethod
    def create_user(cls, info: str, phone_number: str):
        """Creates a new user
        Args:
            info (str): Information provided by the user
            phone_number (str): Phone number to send the message
        """
        lines = info.split("\n")
        if (len(lines) != 3) or \
           ("email:" not in lines[1]) or \
           ("password: " not in lines[2]):
            WhatsAppSender.message("Please copy the user template and edit it.", phone_number)
            return
        email = lines[1].split(":")[1].strip()
        password = lines[2].split(":")[1].strip()
        if "@" not in email or not email.endswith(".com"):
            WhatsAppSender.message("You have entered an invalid email", phone_number)
            return
        users = models.storage.search("User", email=email)
        users.extend(models.storage.search("User", phone=phone_number))
        if users:
            WhatsAppSender.message(f"{users[0].email} has already been registered", phone_number)
            return
        user = User(email, password, phone_number)
        models.storage.save()
        WhatsAppSender.message(f"{user.email} has just been registered", phone_number)

    @classmethod
    def update_user(cls, info: str, phone_number: str):
        """Updates user details
        Args:
            info (str): Information provided by the user
            phone_number (str): Phone number to send the message
        """
        lines = info.split("\n")
        if (len(lines) != 6) or \
           ("email:" not in lines[1]) or \
           ("password:" not in lines[5]) or \
           (info.count(":") < 5):
            WhatsAppSender.message("Please copy the update template and edit it.", phone_number)
            return
        email = lines[1].split(":")[1].strip()
        account = lines[2].split(":")[1].strip()
        bank = lines[3].split(":")[1].strip()
        sort = lines[4].split(":")[1].strip()
        password = lines[5].split(":")[1].strip()

        users = models.storage.search("User", phone=phone_number)
        if users:
            user = users[0]
            if user.password == password:
                if user.email != email and "@" in email and email.endswith(".com"):
                    user.email = email
                    WhatsAppSender.message(f"Email {user.email} was just updated.", phone_number)
                else:
                    WhatsAppSender.message(f"Email was not updated.", phone_number)
                if account and bank and sort:
                    user.update_bank_info(account, bank, sort)
                    WhatsAppSender.message("Bank information was just been updated", phone_number)
                else:
                    WhatsAppSender.message("Bank information was not updated", phone_number)
                models.storage.save()
            else:
                msg = "You passed a wrong password"
                WhatsAppSender.message(msg, phone_number)
        else:
            msg = "You have not been registered.\n" \
                  "Prompt - *register*"
            WhatsAppSender.message(msg, phone_number)

    @classmethod
    def message(cls, message: str, phone_number: str):
        """Sends message to the phone number
        Args:
            message (str): Custom string message to send to number
            phone_number (str): Phone number to send the message.
        """        
        headers = {"Authorization": f"Bearer {cls.authorisation}",
                   "Content-Type": "application/json"}
        json = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": f"{phone_number}",
            "type": "text",
            "text": {
                "preview_url": False,
                "body": message
                }
            }
        
        url = f"https://graph.facebook.com/{getenv('WHATSAPP_API_VERSION')}" \
              f"/{getenv('WHATSAPP_PHONE_ID')}/messages"
        
        requests.post(url, json=json, headers=headers)
