#!/usr/bin/python3
"""Module containing paystack payment integration
"""
from flask import Blueprint, request
import hmac
import hashlib
from os import getenv

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
        return "Error: No Signature", 401

    if pay_sign == signature.hexdigest():
        json_data = request.get_json()
        if json_data["event"] == "charge.success":
            order_id = json_data["data"]["reference"]
            status = json_data["data"]["status"]
        return "Received", 200
    return "Error: Invalid Signature", 403

