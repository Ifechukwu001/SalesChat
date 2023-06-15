#!/usr/bin/env python3
"""WhatsApp Model
"""
import models
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
                    if "hello" in body.lower():
                        WhatsAppSender.hello(phone_number)
                        WhatsAppSender.options(phone_number)
                    

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
    def message(cls, message: str, phone_number: str):
        """Sends hello to the phone number
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
