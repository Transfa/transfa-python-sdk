import json
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


@pytest.fixture()
def valid_webhook_payload():
    """
    :return: a valid webhook payload
    """

    with open("tests/valid_webhook_payload.json") as f:
        return json.load(f)


@pytest.fixture()
def invalid_webhook_payload():
    """
    :return: an invalid webhook payload
    """

    with open("tests/invalid_webhook_payload.json") as f:
        return json.load(f)
