import logging
from enum import Enum

import requests


class MoyklassApiException(Exception):
    def __init__(self, message=None):
        self.message = message
        super().__init__(message)


class PaymentOptype(Enum):
    INCOME = "income"
    DEBIT = "debit"
    REFUND = "refund"


class MoyklassApi:
    def __init__(self, api_key, base_url="https://api.moyklass.com"):
        self.base_url = base_url
        self.api_key = api_key
        self.token = None

    def set_token(self):
        data = {"apiKey": self.api_key}
        r = self._make_request("POST", "v1/company/auth/getToken", data=data)
        self.token = r["accessToken"]

    def revoke_token(self):
        self._make_request("POST", "v1/company/auth/revokeToken")
        self.token = None

    def _make_request(self, method, path, data=None, params=None):
        url = f"{self.base_url}/{path}"

        headers = None
        if self.token is not None:
            headers = dict()
            headers["x-access-token"] = self.token    

        logging.debug(
            f"Sending {method} request to {url} with headers: {headers}; query params: {params}; data: {data}"
        )
        try:
            r = requests.request(method, url, headers=headers, json=data, params=params)
            r.raise_for_status()
        except requests.TooManyRedirects:
            raise MoyklassApiException("Too many redirects")
        except requests.HTTPError as err:
            raise MoyklassApiException(f"HTTPError is occured, and it is {err}")
        except requests.Timeout:
            raise MoyklassApiException("Timeout error. Try again later.")
        except requests.ConnectionError:
            raise MoyklassApiException("Connection is lost, try again later.")

        logging.debug(f"Response: {r.status_code}, {r.content}")

        try:
            response_data = r.json()
        except requests.JSONDecodeError:
            response_data = ""

        return response_data

    def __enter__(self):
        self.set_token()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.revoke_token()

    def get_payments(
        self,
        created_at=None,
        date=None,
        summa=None,
        invoice_id=None,
        optype=None,
        payment_type_id=None,
        include_user_subscriptions=False,
        user_id=None,
        filial_id=None,
        append_invoices=False,
        offset=0,
        limit=100,
    ):
        params = {}
        if created_at is not None:
            params["createdAt"] = created_at

        if date is not None:
            params["date"] = date

        if summa is not None:
            params["summa"] = summa

        if invoice_id is not None:
            params["invoiceId"] = invoice_id

        if optype is not None:
            decoded_optype = []
            for el in optype:
                if isinstance(el, PaymentOptype):
                    decoded_optype.append(el.value)

            if len(decoded_optype):
                params["optype"] = decoded_optype

        if payment_type_id is not None:
            params["paymentTypeId"] = payment_type_id

        if include_user_subscriptions:
            params["includeUserSubscriptions"] = "true"
        else:
            params["includeUserSubscriptions"] = "false"

        if user_id is not None:
            params["userId"] = user_id

        if filial_id is not None:
            params["filialId"] = filial_id

        if append_invoices:
            params["appendInvoices"] = "true"
        else:
            params["appendInvoices"] = "false"

        params["offset"] = offset
        params["limit"] = limit

        return self._make_request("GET", "v1/company/payments", params=params)

    def get_user(self, user_id):
        path = f"v1/company/users/{user_id}"
        return self._make_request("GET", path)
