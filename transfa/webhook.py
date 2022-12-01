import hmac
import hashlib
import json

from transfa import private_secret
from transfa.enums import TransfaHeadersIdentifiers


class Webhook:
    def __init__(self):
        if private_secret is None:
            raise NotImplementedError(
                "Can't work without private secret for security reasons."
            )
        self.webhook_token = private_secret

    def sign_body(self, body, algorithm=hashlib.sha512):
        secret = self.webhook_token.encode("utf-8")

        if not isinstance(body, bytes):
            body = body.encode("utf-8")

        signature = hmac.new(secret, body, digestmod=algorithm)

        return signature.hexdigest()

    def has_data_not_tempered(self, body, transfa_api_signature):

        body = json.dumps(body)
        signature = self.sign_body(body)
        return signature == transfa_api_signature

    def verify(self, headers, body):
        signature = headers.get(TransfaHeadersIdentifiers.webhook_signature)

        if signature is None:
            raise NotImplementedError(
                "No signature provided. Contact the technical support."
            )

        if self.has_data_not_tempered(body, signature):
            return body

        return None


webhook = Webhook()
