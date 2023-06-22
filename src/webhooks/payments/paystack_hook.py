#!/usr/bin/python3
"""Module containing paystack payment integration
"""
import models
from flask import Blueprint, request
import hmac
import hashlib
from os import getenv
import threading
from models.whatsapp import WhatsAppSender

paystack = Blueprint("paystack", __name__)


@paystack.route("/payment", methods=["POST"])
def payment():
    """Webhook for the Paystack API"""
    pay_sign = request.headers.get("x-paystack-signature")
    key = getenv("SC_PAYSTACK_SECRET")
    msg = request.get_data()
    signature = hmac.new(key.encode(), digestmod=hashlib.sha512)
    signature.update(msg)

    if pay_sign is None:
        return "Unauthorised", 401

    if pay_sign == signature.hexdigest():
        json_data = request.get_json()
        thread = threading.Thread(target=process, args=(json_data,))
        thread.start()
        return "Received", 200
    return "Forbidden", 403

def process(data: dict):
    """Processes event
    Args:
        data (dict): Event Data to process
    """
    models.storage.reload()
    if data["event"] == "charge.success":
        order_id = data["data"]["reference"]
        status = data["data"]["status"]

        order_detail = models.storage.get("OrderDetail", order_id)
        if (status == "success") and order_detail and \
           (order_detail.payment_verified != True):
            order_detail.payment_verified = True
            data = {"field": "order",
                    "order_id": order_id}
            WhatsAppSender.process(data)
            models.storage.save()
    models.storage.close()
