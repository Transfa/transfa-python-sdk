# Transfa Python SDK

The Transfa Python SDK provides methods and resources to the Transfa API for applications written in Python. 

## Documentation

You can check the [Python API documentation](https://docs.transfapp.com/sdk/python/) for more details about the API. 

## Installation

Run the following command:

```shell
pip install --upgrade transfa
```

## Requirements
- Python 3.8+ 

## Getting started

### Request a payment

When sending a payment request to Transfa's API it is important to provide a unique idempotency key. That key will be in the header of each payment request. An idempotency key is a key that will make each payment request unique thus preventing us from creating the same payment object several times in the database in case of a network error or an outage. No matter how many times you send a request with the same idempotency key, it won't change the result of the first executed one.

Here is an example:

```python
import uuid

from transfa.api_client import client

client.api_key = "ak_test_..."

response = client.Payment.request_payment({
        "account_alias": "60201010",
        "amount": 5000,
        "mode": "mtn-benin",
        "webhook_url": "https://your_app_url.domain/your_webhook_endpoint/" # Optional
    },
    idempotency_key=uuid.uuid4().hex)

# Process the response's body
print(response.text)
```

### Retrieve a single payment

```python
from transfa.api_client import client

client.api_key = "ak_test_..."

response = client.Payment.retrieve(payment_id="28dc22751e854b86a6a1d8ded87a83")
print(response.text)
```

### Get the status of a payment

```python
from transfa.api_client import client

client.api_key = "ak_test_..."

response = client.Payment.status(payment_id="28dc22751e854b86a6a1d8ded87a83")
print(response)
```

### Refund a payment

```python
from transfa.api_client import client

client.api_key = "ak_test_..."

response = client.Payment.refund(payment_id="28dc22751e854b86a6a1d8ded87a83")
print(response.text)
```

### List all payments

```python
from transfa.api_client import client

client.api_key = "ak_test_..."

response = client.Payment.list()
print(response.text)
```

### Verify webhook
We will notify you each time there is be an update about your payments at the condition that your Organization supports the webhook feature (check on your organization's dashboard if you wan't to activate it) and that you provided a webhook url at which we can send the datas when sending the payment request. This will help you to automatically get an update without having to periodically send GET requests to our API.

But before you process the payload of a Webhook request, you must first verify that it is coming from Transfa and not from an unknown server acting like Transfa's server. Each webhook request will come with a parameter in the headers named `X-Webhook-Transfa-Signature`. You'll use that signature to make sure that the request is coming from us.

We provided you with a class called `Webhook` that will handle the whole verification underneath. All you have to do is creating an instance of the class with the required parameters.
Here is an example of how you would do it with Django Rest Framework.

```python
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from transfa.webhook import Webhook

# Do not save the secret key in plain text in your code, set it instead as an environment variable.
secret_key = 'ps_test:...'

@api_view(["POST"])
def webhook_endpoint(request):
    body = request.data
    
    # Will return either the payload of the request or None.
    webhook = Webhook(webhook_token=secret_key, body=body, headers=request.headers)
    verified = webhook.verify()

    if verified is None:
        return Response({"detail": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    # Process Webhook payload
    # ...
    # ...

    # Note: Make sure you send an HTTP 200 OK status after processing the payload
    # We have a retry mechanism that will send the webhook request up to 3 time in case you return
    # a status code different than 200.
    return Response({"detail": True}, status=status.HTTP_200_OK)
```
