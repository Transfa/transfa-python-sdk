import uuid
from http import HTTPStatus

import responses
from responses import matchers

from transfa.api_client import client
from transfa.configs.version import VERSION

client.api_key = "ak_live_123"
API_URL = "https://api.transfapp.com/api/v1/optimus/payment/"


def paginator_response(data):
    return {"count": len(data), "results": data}


@responses.activate
def test_request_payment(payment):
    """
    Given some data, test that the request for a payment is sent correctly.
    """
    idempotency_key = uuid.uuid4().hex

    responses.add(
        responses.POST,
        API_URL,
        json=payment,
        status=HTTPStatus.CREATED,
        match=[
            matchers.header_matcher(
                {
                    "Authorization": f"{client.api_key}",
                    "accept": "application/json",
                    "content-type": "application/json;charset=utf-8",
                    "Idempotency-Key": idempotency_key,
                    "user-agent": "Transfa API SDK-Python/%s" % VERSION,
                }
            )
        ],
    )
    data = {"account_alias": "60201010", "amount": 5000, "mode": "mtn-benin"}

    response = client.Payment.request_payment(data, idempotency_key=idempotency_key)

    assert response.status_code == HTTPStatus.CREATED
    response_data = response.json()

    assert response_data["account_alias"] == data["account_alias"]
    assert response_data["amount"] == data["amount"]
    assert response_data["mode"] == data["mode"]
    assert response_data["type"] == "request-payment"


@responses.activate
def test_list_payments(payments):
    """
    Given some data, test that the request to list payment is sent correctly..
    """

    responses.add(
        responses.GET,
        API_URL,
        json=paginator_response(payments),
        status=HTTPStatus.OK,
        match=[
            matchers.header_matcher(
                {
                    "Authorization": f"{client.api_key}",
                    "user-agent": "Transfa API SDK-Python/%s" % VERSION,
                }
            )
        ],
    )

    response = client.Payment.list()

    assert response.status_code == HTTPStatus.OK
    response_data = response.json()

    assert response_data["count"] == 1


@responses.activate
def test_retrieve_payment(payment):
    """
    Given some data, test that the request to list payment is sent correctly..
    """

    responses.add(
        responses.GET,
        f"{API_URL}{payment['id']}/",
        json=payment,
        status=HTTPStatus.OK,
        match=[
            matchers.header_matcher(
                {
                    "Authorization": f"{client.api_key}",
                    "user-agent": "Transfa API SDK-Python/%s" % VERSION,
                }
            ),
            matchers.query_param_matcher({}),
        ],
    )

    response = client.Payment.retrieve(payment["id"])

    assert response.status_code == HTTPStatus.OK
    response_data = response.json()

    assert response_data["id"] == payment["id"]


@responses.activate
def test_refund_payment(payment):
    """
    Given some data, test that the request to list payment is sent correctly..
    """

    responses.add(
        responses.POST,
        f"{API_URL}{payment['id']}/refund/",
        json=payment,
        status=HTTPStatus.OK,
        match=[
            matchers.header_matcher(
                {
                    "Authorization": f"{client.api_key}",
                    "user-agent": "Transfa API SDK-Python/%s" % VERSION,
                }
            )
        ],
    )

    response = client.Payment.refund(payment["id"])

    assert response.status_code == HTTPStatus.OK
    response_data = response.json()

    assert response_data["id"] == payment["id"]
