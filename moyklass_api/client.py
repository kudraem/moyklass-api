import logging

import requests


class MoyklassApiException(BaseException):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


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

        headers = {}
        if self.token is not None:
            headers["x-access-token"] = self.token
        else:
            headers = None

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
        created_at=[],
        date=[],
        summa=[],
        invoice_id=None,
        optype=[],
        payment_type_id=None,
        include_user_subscriptions=False,
        user_id=None,
        filial_id=[],
        append_invoices=False,
        offset=0,
        limit=100,
    ):
        params = {}
        if len(created_at):
            params["createdAt"] = created_at

        if len(date):
            params["date"] = date

        if len(summa):
            params["summa"] = summa

        if invoice_id is not None:
            params["invoiceId"] = invoice_id

        if len(optype):
            params["optype"] = optype

        if payment_type_id is not None:
            params["paymentTypeId"] = payment_type_id

        if include_user_subscriptions:
            params["includeUserSubscriptions"] = "true"
        else:
            params["includeUserSubscriptions"] = "false"

        if user_id is not None:
            params["userId"] = user_id

        if len(filial_id):
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
