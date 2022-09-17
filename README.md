# Transfa Python SDK

The Transfa Python SDK provides methods and resources to the Transfa API for applications written in Python. 

## Documentation

You can check the[Python API documentation](https://docs.transfapp.com/sdk/python/) for more details about the API. 

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
