import hmac
import hashlib
import json

from transfa.api_resources.webhook import WebhookResource
from transfa.utils.helpers import get_random_string


class WebhookData:
    def __init__(self):
        self.valid_webhook_token = get_random_string(64)
        self.invalid_webhook_token = get_random_string(64)

    def generate_signature(self, body, webhook_token, algorithm=hashlib.sha512):
        body = json.dumps(body)
        secret = webhook_token.encode("utf-8")

        if not isinstance(body, bytes):
            body = body.encode("utf-8")

        signature = hmac.new(secret, body, digestmod=algorithm)

        return signature.hexdigest()


def test_valid_webhook_signature(valid_webhook_payload):
    webhook_data = WebhookData()
    signature = webhook_data.generate_signature(
        valid_webhook_payload, webhook_data.valid_webhook_token
    )

    webhook = WebhookResource(
        webhook_token=webhook_data.valid_webhook_token,
        body=valid_webhook_payload,
        headers={"X-Webhook-Transfa-Signature": signature},
    )

    verified = webhook.verify()

    assert verified == valid_webhook_payload


def test_invalid_webhook_signature(valid_webhook_payload, invalid_webhook_payload):
    webhook_data = WebhookData()
    invalid_signature = webhook_data.generate_signature(
        invalid_webhook_payload, webhook_data.valid_webhook_token
    )

    webhook = WebhookResource(
        webhook_token=webhook_data.valid_webhook_token,
        body=valid_webhook_payload,
        headers={"X-Webhook-Transfa-Signature": invalid_signature},
    )

    verified = webhook.verify()

    assert not verified


def test_valid_webhook_token(valid_webhook_payload):
    webhook_data = WebhookData()
    valid_signature = webhook_data.generate_signature(
        valid_webhook_payload, webhook_data.valid_webhook_token
    )

    webhook = WebhookResource(
        webhook_token=webhook_data.valid_webhook_token,
        body=valid_webhook_payload,
        headers={"X-Webhook-Transfa-Signature": valid_signature},
    )

    verified = webhook.verify()

    assert verified == valid_webhook_payload


def test_invalid_webhook_token(valid_webhook_payload):
    webhook_data = WebhookData()
    valid_signature = webhook_data.generate_signature(
        valid_webhook_payload, webhook_data.valid_webhook_token
    )

    webhook = WebhookResource(
        webhook_token=webhook_data.invalid_webhook_token,
        body=valid_webhook_payload,
        headers={"X-Webhook-Transfa-Signature": valid_signature},
    )

    verified = webhook.verify()

    assert not verified
