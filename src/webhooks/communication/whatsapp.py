#!?usr/bin/env python3
"""Whatsapp Webhook"""
from models.whatsapp import WhatsAppSender
from flask import Blueprint, request
from os import getenv
import hashlib
import hmac
import threading

greenapp = Blueprint("whatsapp", __name__)


@greenapp.route("/whatsapp")
def verify():
    """Verifies the webhook on WhatsApp cloud API"""
    mode = request.args.get("hub.mode")
    challenge = request.args.get("hub.challenge")
    token = request.args.get("hub.verify_token")

    if mode == "subscribe" and token == getenv("WHATSAPP_VERIFY"):
        return challenge
    return "Forbidden", 403
    
@greenapp.route("/whatsapp", methods=["POST"])
def event():
    """Event notifications on WhatsApp"""

    signature = request.headers.get("X-Hub-Signature-256")
    signature = signature[7:]

    payload = request.get_data()
    _signature = hmac.new(getenv("WHATSAPP_SECRET").encode(), digestmod=hashlib.sha256)
    _signature.update(payload)
    _signature = _signature.hexdigest()

    if signature == _signature:
        data = request.get_json()

        if data["object"] == "whatsapp_business_account":
            if data["entry"][0]["changes"][0]["field"] == "messages":
                information = data["entry"][0]["changes"][0]
                thread = threading.Thread(target=WhatsAppSender.process, args=(information,))
                thread.start()

        print(information)
        return "Recieved", 200
    else:
        return "Forbidden", 403
