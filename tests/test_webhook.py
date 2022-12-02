from transfa.webhook import Webhook

valid_webhook_token = "WjmCvKDSge1QxNnANoqj1dSdpKQAvK5Gy7VSjwsizWSnUcUzzA61T7XgBMhW1rRv"
invalid_webhook_token = "DoQoxCi2b5omxTl5ESnapZcNUiYrzlhan5Za4nNWWpHAGbc6GFHHVCwKZxt5K9Xu"

webhook_data = {
    "id": "2588efb42dc7436f890c1b8a0aabd72f",
    "event": "payment:processing",
    "payment": "GYKU0QL4KX",
    "created": "2022-12-02T10:54:08.511427+00:00",
    "updated": "2022-12-02T10:54:08.511435+00:00"
}

invalid_webhook_data = {
    "id": "2588efb42dc",
    "event": "payment:success",
    "payment": "0QL4KX",
    "created": "2021-12-02T10:54:08.511427+00:00",
    "updated": "2021-12-02T10:54:08.511435+00:00"
}
valid_signature = "ef772c05c9c572d78f3b41e5dd84df04fb8174606746da015c651e296e1c39b9794efa5f173e993dd356c36ab4ca" \
                  "e2e583fa9f87ac9b49184cb86cc77111a22e"
invalid_signature = "1273fcf7eeb4444187c4f111d6ca7695e228c8761363c82448529a2fe7100986f78bb1909492c3c1cbe2165cab" \
                    "287bb557e612f8739ce351f25236fae39db829"


def test_valid_webhook_signature():
    webhook = Webhook(webhook_token=valid_webhook_token, body=webhook_data, headers={
        "X-Webhook-Transfa-Signature": valid_signature
    })

    verified = webhook.verify()

    assert verified == webhook_data


def test_invalid_webhook_signature():
    webhook = Webhook(webhook_token=valid_webhook_token, body=webhook_data, headers={
        "X-Webhook-Transfa-Signature": invalid_signature
    })

    verified = webhook.verify()

    assert not verified


def test_valid_webhook_token():
    webhook = Webhook(webhook_token=valid_webhook_token, body=webhook_data, headers={
        "X-Webhook-Transfa-Signature": valid_signature
    })

    verified = webhook.verify()

    assert verified == webhook_data


def test_invalid_webhook_token():
    webhook = Webhook(webhook_token=invalid_webhook_token, body=webhook_data, headers={
        "X-Webhook-Transfa-Signature": valid_signature
    })

    verified = webhook.verify()

    assert not verified
