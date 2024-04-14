import hmac
import hashlib
import json

from transfa import private_secret
from transfa.types.enums import TransfaHeadersIdentifiers


class WebhookResource:
    def __init__(self, webhook_token=private_secret, body=None, headers=None):
        if webhook_token is None:
            raise NotImplementedError(
                "Can't work without private secret for security reasons."
            )

        if body is None:
            raise NotImplementedError("Can't work without the body of the request.")

        if headers is None:
            raise NotImplementedError("Can't work without the headers.")

        if isinstance(body, bytes):
            body = body.decode("utf-8")
            body = json.loads(body)

        self.webhook_token = webhook_token
        self.headers = headers
        self.body = body

    def sign_body(self, body, algorithm=hashlib.sha512):
        secret = self.webhook_token.encode("utf-8")

        if not isinstance(body, bytes):
            body = body.encode("utf-8")

        signature = hmac.new(secret, body, digestmod=algorithm)

        return signature.hexdigest()

    def has_data_not_tempered(self, body, transfa_api_signature):
        if isinstance(body, dict):
            body = json.dumps(body)

        signature = self.sign_body(body)
        return signature == transfa_api_signature

    def verify(self):
        signature = self.headers.get(TransfaHeadersIdentifiers.webhook_signature.value)

        if signature is None:
            raise NotImplementedError(
                "No signature provided. Contact the technical support."
            )

        if self.has_data_not_tempered(self.body, signature):
            return self.body

        return None
