import json

from requests import request

from transfa import api_key, api_base
from transfa.api_resources.payments import PaymentResource

from transfa.configs.version import VERSION


class TransfaAPIClient:
    _base_url = api_base
    __version__ = VERSION

    def __init__(
        self,
        timeout=5,
        verify_ssl=True,
    ):
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.api_key = api_key
        self.Payment = PaymentResource(self)

    def _get_url(self, endpoint):
        """Get URL for requests"""
        url = self._base_url

        # Making sure URL is in the right format.
        if url.endswith("/"):
            url = url[:-1]
        if endpoint.startswith("/"):
            endpoint = endpoint[:-1]

        return f"{url}/{endpoint}"

    def _request(self, method, endpoint, data=None, params=None, **kwargs):
        """Do requests"""
        if params is None:
            params = {}

        url = self._get_url(endpoint)
        headers = {
            "user-agent": "Transfa API SDK-Python/%s" % self.__version__,
            "accept": "application/json",
            "Authorization": f"{self.api_key}",
        }

        if "headers" in kwargs:
            headers = {**kwargs.pop("headers"), **headers}

        if data is not None:
            data = json.dumps(data, ensure_ascii=False).encode("utf-8")
            headers["content-type"] = "application/json;charset=utf-8"

        return request(
            method=method,
            url=url,
            verify=self.verify_ssl,
            params=params,
            data=data,
            timeout=self.timeout,
            headers=headers,
            **kwargs,
        )

    def post(self, endpoint, data=None, **kwargs):
        """POST requests"""
        return self._request("POST", endpoint, data, **kwargs)

    def get(self, endpoint, **kwargs):
        """GET requests"""
        return self._request("GET", endpoint, **kwargs)


client = TransfaAPIClient()
