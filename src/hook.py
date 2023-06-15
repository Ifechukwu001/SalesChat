#!/usr/bin/env python3
"""Module containing the webhook"""
from flask import Flask
from webhooks.payments.paystack_hook import paystack
from webhooks.communication.whatsapp import greenapp

app = Flask(__name__)
app.register_blueprint(paystack)
app.register_blueprint(greenapp)

if __name__ == "__main__":
    app.run(port=5000)
