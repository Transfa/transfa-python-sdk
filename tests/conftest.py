import json
import os
import pytest


@pytest.fixture()
def payments():
    """
    :return: list of payments
    """
    with open("tests/payments.json") as f:
        return json.load(f)


@pytest.fixture()
def payment(payments):
    """
    :return: a payment object
    """
    return payments[0]
