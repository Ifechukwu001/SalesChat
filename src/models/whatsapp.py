#!/usr/bin/env python3
"""WhatsApp Model
"""
import models
from models.user import User
from models.product import Product
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
                    elif body.lower().startswith("search"):
                        WhatsAppSender.search(body, phone_number)
                elif message_type == "image":
                    caption = message[0]["image"]["caption"]
                    image_id = message[0]["image"]["id"]
                    if caption.lower().startswith("product"):
                        WhatsAppSender.create_product(image_id, caption, phone_number)
                elif message_type == "interactive":
                    interactive = message[0]["interactive"]
                    inter_type = interactive["type"]
                    if inter_type == "button_reply":
                        object_id = interactive["button_reply"]["id"]
                        title = interactive["button_reply"]["title"]
                        if title.lower().startswith("add-cart"):
                            WhatsAppSender.add_cart(object_id, phone_number)
                    
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
                      "category: (goods/service/digital)\n"\
                      "quantity: "
                WhatsAppSender.message(msg, phone_number)
                msg = "Ps: Price is in NGN, "\
                      "description & quantity (digital/service) are optional"
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
    def create_product(cls, media_id: str, info: str, phone_number: str):
        """Creates a new product
        Args:
            info (str): Information provided by the user
            phone_number (str): Phone number to send the message
        """
        lines = info.split("\n")
        if (len(lines) != 6) or \
           ("name:" not in lines[1]) or \
           ("description:" not in lines[2]) or \
           ("price:" not in lines[3]) or \
           ("category:" not in lines[4]) or \
           ("quantity:" not in lines[5]):
            WhatsAppSender.message("Please copy the product template and edit it.", phone_number)
        name = lines[1].split(":")[1].strip()
        desc = lines[2].split(":")[1].strip()
        price = lines[3].split(":")[1].strip()
        category = lines[4].split(":")[1].strip()
        quantity = lines[5].split(":")[1].strip()

        if not price.isdigit():
            WhatsAppSender.message("Price must be a number in NGN.", phone_number)
            return
        if category not in ["goods", "service", "digital"]:
            WhatsAppSender.message("Category must be one of 'goods', 'service', 'digital'", phone_number)
            return
        if category == "goods" and not quantity.isdigit():
            WhatsAppSender.message("Quantity was not set.", phone_number)
            return
        users = models.storage.search("User", phone=phone_number)
        if users:
            user = users[0]
            product = user.create_product(name, desc, int(price), int(quantity), category)
            product.thumbnail = media_id
            models.storage.save()
            WhatsAppSender.message(f"Product '{product.name}' has been added to the MarketPlace", phone_number)
        else:
            WhatsAppSender.message("You have not been registered", phone_number)

    @classmethod
    def search(cls, info: str, phone_number: str):
        """Searches for a product
        Args:
            info (str): Information provided by the user
            phone_number (str): Phone number to send the message
        """
        query = info.split(None, 1)
        if len(query) > 1:
            query = query[1].strip()
        else:
            WhatsAppSender.message("There is no product match", phone_number)
            return
        criterion = Product.name.contains(query)
        products = models.storage.search("Product", criterion)
        if len(products) < 4:
            criterion = Product.description.contains(query)
            extra = models.storage.search("Product", criterion)
            products.extend(extra)
        filter_func = lambda product: product.is_available(1)
        products = list(filter(filter_func, set(products)))

        if products:
            replys = []
            for product in products[:5]:
                msg = f"Name: {product.name}\n" \
                      f"Description: {product.description}\n\n" \
                      f"Price: NGN {product.price}"
                WhatsAppSender.image_message(phone_number,
                                             media_id=product.thumbnail,
                                             caption=msg)
                reply = {"title": f"add-cart {product.name}", "id": product.id}
                replys.append(reply)

            WhatsAppSender.reply_message(phone_number, replys)
        else:
            WhatsAppSender.message("There is no product match", phone_number)

    @classmethod
    def add_cart(cls, product_id: str, phone_number: str):
        """Adds a product to cart
        Args:
            product_id (str): Product ID of product to add
            info (str): Information provided by the user
            phone_number (str): Phone number to send the message
        """
        users = models.storage.search("User", phone=phone_number)
        if users:
            user = users[0]
            user.add_to_cart(product_id)
            models.storage.save()
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

    @classmethod
    def image_message(cls, phone_number: str, media_id: str = None,
                      media_url: str = None, caption: str = None):
        """Sends an image message to the phone number
        Args:
            phone_number (str): Phone number to send the message.
            media_id (str): Whatsapp Media object ID
            media_url (str): Public URL of the Media object
            caption (str): Message attached to the image.
        """        
        headers = {"Authorization": f"Bearer {cls.authorisation}",
                   "Content-Type": "application/json"}
        if media_id:
            json = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": f"{phone_number}",
                "type": "image",
                "image": {
                    "id": media_id,
                    "caption": caption
                    }
                }
        elif media_url:
            json = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": f"{phone_number}",
            "type": "image",
            "image": {
                "url": media_url,
                "caption": caption
                }
            }
        else:
            raise SyntaxError("You need to pass media_id or media_url")
        
        url = f"https://graph.facebook.com/{getenv('WHATSAPP_API_VERSION')}" \
              f"/{getenv('WHATSAPP_PHONE_ID')}/messages"
        
        requests.post(url, json=json, headers=headers)

    @classmethod
    def reply_message(cls, phone_number: str, replys: list[dict]):
        """Sends a reply interactive message to the phone number
        Args:
            phone_number (str): Phone number to send the message.
            replys (list[dict]): List of reply objects
        """        
        headers = {"Authorization": f"Bearer {cls.authorisation}",
                   "Content-Type": "application/json"}
        buttons = [{"type": "reply", "reply": reply} for reply in replys]

        json = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": f"{phone_number}",
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": "Select your choice to proceed to checkout"
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
        
        url = f"https://graph.facebook.com/{getenv('WHATSAPP_API_VERSION')}" \
              f"/{getenv('WHATSAPP_PHONE_ID')}/messages"
        
        requests.post(url, json=json, headers=headers)
