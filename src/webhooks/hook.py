#!/usr/bin/env python3
"""Module containing the webhook"""
from flask import Flask
from payments.paystack_hook import paystack

app = Flask(__name__)
app.register_blueprint(paystack)

if __name__ == "__main__":
    app.run(port=5000)
