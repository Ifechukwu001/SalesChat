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
        models.storage.reload()
        if information.get("field") == "messages":
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
                    elif body.lower().startswith("cart"):
                        WhatsAppSender.cart(phone_number)
                    elif body.lower().startswith("product"):
                        WhatsAppSender.product(phone_number)
                    elif body.lower().startswith("checkout"):
                        WhatsAppSender.checkout(phone_number)
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
                elif message_type == "document":
                    caption = message[0]["document"]["caption"]
                    document_id = message[0]["document"]["id"]
                    if caption.lower().startswith("product"):
                        WhatsAppSender.save_product_file(document_id, caption,
                                                         phone_number)
        elif information.get("field") == "order":
            order_id = information.get("order_id")
            WhatsAppSender.order(order_id)
        models.storage.close()
                    
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
            msg = "Please copy the product template and edit it."
            WhatsAppSender.message(msg, phone_number)
        name = lines[1].split(":")[1].strip()
        desc = lines[2].split(":")[1].strip()
        price = lines[3].split(":")[1].strip()
        category = lines[4].split(":")[1].strip()
        quantity = lines[5].split(":")[1].strip()

        if not price.isdigit():
            WhatsAppSender.message("Price must be a number in NGN.",
                                   phone_number)
            return
        if category not in ["goods", "service", "digital"]:
            msg = "Category must be one of 'goods', 'service', 'digital'"
            WhatsAppSender.message(msg, phone_number)
            return
        if category == "goods" and not quantity.isdigit():
            WhatsAppSender.message("Quantity was not set.", phone_number)
            return
        elif category != "goods":
            quantity = "1"
        users = models.storage.search("User", phone=phone_number)
        if users:
            user = users[0]
            product = user.create_product(name, desc, int(price),
                                          int(quantity), category)
            product.thumbnail = media_id
            models.storage.save()
            msg = f"Product '{product.name}' has been added to the MarketPlace"
            WhatsAppSender.message(msg, phone_number)
            if category == "digital":
                msg = "Send the Digital content as a document " \
                      "with the caption: product <Product full name>"
                WhatsAppSender.message(msg, phone_number)
        else:
            msg = "You have not been registered.\n" \
                  "Prompt - *register*"
            WhatsAppSender.message(msg, phone_number)

    @classmethod
    def product(cls, phone_number: str):
        """Displays all products a user has created
        Args:
            phone_number (str): Phone number to message
        """
        users = models.storage.search("User", phone=phone_number)
        if users:
            user = users[0]
            for product in user.products:
                prod_name = product.name
                prod_desc = product.description
                prod_thumbnail = product.thumbnail
                msg = f"Name: {prod_name}\n" \
                      f"Description: {prod_desc}"
                WhatsAppSender.image_message(phone_number, prod_thumbnail,
                                             caption=msg)
        else:
            msg = "You have not been registered.\n" \
                  "Prompt - *register*"
            WhatsAppSender.message(msg, phone_number)

    @classmethod
    def save_product_file(cls, media_id: str, info: str, phone_number: str):
        """Saves the product document
        Args:
            media_id (str): Media ID of the product
            info (str): Information provided by the user
            phone_number (str): Phone number to send the message
        """
        product_name = info.split(None, 1)
        if len(product_name) > 1:
            product_name = product_name[1].strip()
        else:
            WhatsAppSender.message("Product was not found", phone_number)
            return
        users = models.storage.search("User", phone=phone_number)
        if users:
            user = users[0]
            filter_prods = lambda product: product.name == product_name
            products = list(filter(filter_prods, user.products))
            if products:
                product = products[0]
                product.location = media_id
                models.storage.save()
                msg = f"{product_name}'s document has been saved"
                WhatsAppSender.message(msg, phone_number)
            else:
                msg = f"Product '{product_name}' was not found"
                WhatsAppSender.message(msg, phone_number)
        else:
            msg = "You have not been registered.\n" \
                  "Prompt - *register*"
            WhatsAppSender.message(msg, phone_number)

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
            item = user.add_to_cart(product_id)
            item.quantity = 1
            models.storage.save()
            WhatsAppSender.message("Item has been added to cart", phone_number)
        else:
            msg = "You have not been registered.\n" \
                  "Prompt - *register*"
            WhatsAppSender.message(msg, phone_number)

    @classmethod
    def cart(cls, phone_number: str):
        """Displays all products in the cart
        Args:
            phone_number (str): Phone number to message
        """
        users = models.storage.search("User", phone=phone_number)
        if users:
            user = users[0]
            for item in user.cart:
                product = models.storage.get("Product", item.product_id)
                msg = f"Name: {product.name}\n" \
                      f"Description: {product.description}\n" \
                      f"Quantity: {item.quantity}"
                WhatsAppSender.message(msg, phone_number)
        else:
            msg = "You have not been registered.\n" \
                  "Prompt - *register*"
            WhatsAppSender.message(msg, phone_number)

    @classmethod
    def checkout(cls, phone_number: str):
        """Checkout Cart items
        Args:
            phone_number (str): Phone number to message
        """
        users = models.storage.search("User", phone=phone_number)
        if users:
            user = users[0]
            payment_link = user.checkout()
            if payment_link:
                msg = f"Proceed to this link to make payment: {payment_link}"
                WhatsAppSender.message(msg, phone_number)
            else:
                msg = "Could not process checkout: \n"\
                      "You don't have anything in your cart.\n" \
                      "Check previous messages for checkout link."
                WhatsAppSender.message(msg, phone_number)
        else:
            msg = "You have not been registered.\n" \
                  "Prompt - *register*"
            WhatsAppSender.message(msg, phone_number)

    @classmethod
    def order(cls, order_id: str):
        """Processes a finished Order
        Args:
            order_id (str): OrderDetails ID
        """
        order_detail = models.storage.get("OrderDetail", order_id)
        if order_detail:
            user = models.storage.get("User", order_detail.buyer_id)
            phone_number = user.phone
            digital_prods = []
            other_prods = []
            for item in order_detail.items:
                product = models.storage.get("Product", item.product_id)
                if product.category == "digital":
                    digital_prods.append(product)
                else:
                    other_prods.append(product)
            if digital_prods:
                WhatsAppSender.message("Here are your digital products",
                                       phone_number)
                for product in digital_prods:
                    msg = f"Name: {product.name}"
                    WhatsAppSender.document_message(phone_number,
                                                    product.location,
                                                    caption=msg)
            if other_prods:
                msg = "Your goods and services are on its way"
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
                    "text": "Select your choice to proceed"
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
        
        url = f"https://graph.facebook.com/{getenv('WHATSAPP_API_VERSION')}" \
              f"/{getenv('WHATSAPP_PHONE_ID')}/messages"
        
        requests.post(url, json=json, headers=headers)

    @classmethod
    def document_message(cls, phone_number: str, media_id: str = None,
                      media_url: str = None, caption: str = None):
        """Sends an document message to the phone number
        Args:
            phone_number (str): Phone number to send the message.
            media_id (str): Whatsapp Media object ID
            media_url (str): Public URL of the Media object
            caption (str): Message attached to the document.
        """        
        headers = {"Authorization": f"Bearer {cls.authorisation}",
                   "Content-Type": "application/json"}
        if media_id:
            json = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": f"{phone_number}",
                "type": "document",
                "document": {
                    "id": media_id,
                    "caption": caption
                    }
                }
        elif media_url:
            json = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": f"{phone_number}",
            "type": "document",
            "document": {
                "url": media_url,
                "caption": caption
                }
            }
        else:
            raise SyntaxError("You need to pass media_id or media_url")
        
        url = f"https://graph.facebook.com/{getenv('WHATSAPP_API_VERSION')}" \
              f"/{getenv('WHATSAPP_PHONE_ID')}/messages"
        
        requests.post(url, json=json, headers=headers)
