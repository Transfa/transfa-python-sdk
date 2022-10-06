import hmac
import hashlib


def verify_webhook(api_secret_key, data, hmac_header):

    signature = hmac.new(api_secret_key.encode('utf-8'), data, digestmod=hashlib.sha512)
    signature = signature.hexdigest()

    return hmac.compare_digest(signature, hmac_header.encode('utf-8'))
