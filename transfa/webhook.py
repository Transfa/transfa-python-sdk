import hmac
import hashlib


def verify_webhook(secret_key, body, request_header):

    signature = hmac.new(secret_key.encode('utf-8'), body, digestmod=hashlib.sha512)
    signature = signature.hexdigest()

    return hmac.compare_digest(signature, request_header.encode('utf-8'))
