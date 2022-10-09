import hmac
import hashlib
from datetime import datetime


class Webhook:
    def sign_body(self, secret_key, body):

        if not isinstance(body, bytes):
            body = body.encode("utf-8")

        signature = hmac.new(secret_key.encode('utf-8'), body, digestmod=hashlib.sha512)

        return signature.hexdigest()

    def verify_webhook(self, secret_key, body, request_header):

        signature = self.sign_body(secret_key, body)
        verified = hmac.compare_digest(signature, request_header.encode('utf-8'))

        if not verified:
            return False, None

        data = body
        data["created"] = datetime.fromtimestamp(data["created"]).strftime("%m/%d/%Y %H:%M:%S")
        data["update"] = datetime.fromtimestamp(data["update"]).strftime("%m/%d/%Y %H:%M:%S")

        return verified, data


webhook = Webhook()
