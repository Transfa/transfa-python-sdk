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

## Usage

```python
from transfa.api_client import client

client.api_key = "ak_test_..."

response = client.Payment.request_payment({
        "account_alias": "60201010",
        "amount": 5000,
        "mode": "mtn-benin"
    })

print(response.text)
```

## Verify webhook

Before you respond to a Webhook request, you need first to verify that it is coming from Transfa.

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
    
    # Will return True or False and the body of the request that has been slightly modified
    # You should use that data when processing the webhook instead of the previous one
    webhook = Webhook(webhook_token=secret_key, body=body, headers=request.headers)
    verified = webhook.verify()

    if verified is None:
        return Response({"detail": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    # Process Webhook payload
    # ...
    # ...

    return Response({"detail": True}, status=status.HTTP_200_OK)
```