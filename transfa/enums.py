from enum import Enum


class PaymentStatusEnum(Enum):
    completed = "completed"
    processing = "processing"
    pending = "pending"
    failed = "failed"


class PaymentMode(Enum):
    mtn_benin = "mtn-benin"


class PaymentTypeEnum(Enum):
    request_payment = "request-payment"


class PaymentEventHookEnum(Enum):
    processing = "payment:processing"
    failed = "payment:failed"
    success = "payment:success"


class APIKeyPrefix(Enum):
    test = "ak_test"
    live = "ak_live"


class PrivateSecretPrefix(Enum):
    test = "ps_test"
    live = "ps_live"


class TransfaHeadersIdentifiers(Enum):
    webhook_signature = "X-Webhook-Transfa-Signature"
