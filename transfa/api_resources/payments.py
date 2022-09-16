import logging
import uuid

from transfa import get_default_log_message
from transfa.enums import PaymentTypeEnum


class PaymentResource:
    """
        This class contains methods and utils used for interacting with the payment API.
    """
    def __init__(self, api):
        self.api = api
        self.base_url = "api/v1/optimus/payment"

    def request_payment(self, data, **kwargs):
        """
        This method create a payment request on the /payment/ endpoint.
        :param data: a dict with the following information:
            :key account_alias: the phone number of the consumer. Required.
            :key amount: the amount of the payment. Required.
            :key mode: The mode of payment. For the moment, we only supports the MTN Momo Bénin API.
            :key webhook_url: the callback URL.
            :key first_name: First name of the client.
            :key last_name: Last name of the client.
            :key email: Email of the client.
        :param kwargs:
        :return: Response Object.
        """

        # Idempotency key setup in headers
        kwargs['headers'] = {
            "Idempotency-Key": uuid.uuid4()
        }

        data["type"] = PaymentTypeEnum.request_payment.value

        url = f"{self.base_url}/"

        return self.api.post(url, data, **kwargs)

    def list(self, **kwargs):
        """
        :param kwargs:
        :return:  Response object.
        """
        return self.api.get(f"{self.base_url}/", **kwargs)

    def retrieve(self, payment_id, **kwargs):
        """
        :param kwargs:
        :return:  Response object.
        """
        return self.api.get(f"{self.base_url}/{payment_id}/", **kwargs)

    def refund(self, payment_id, **kwargs):
        """
        :param kwargs:
        :return:  Response object.
        """
        return self.api.post(f"{self.base_url}/{payment_id}/refund/", **kwargs)

    def status(self, payment_id):
        """
        :param payment_id: The payment id of the payment.
        :return: A a tuple of the status and financial status of the payment. => (status, financial_status)
        """
        response = self.retrieve(payment_id)
        if response.status_code != 200:
            logging.error(get_default_log_message(response))

        response_data = response.json()

        return response_data.get('status'), response_data.get('financial_status')

