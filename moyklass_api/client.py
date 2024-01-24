import logging
from enum import Enum
from typing import Any, Dict, List

import requests


class MoyklassApiException(Exception):
    def __init__(self, message: str = None) -> None:
        """
        Exception for Moyklass API errors.

        Args:
            message (str, optional): Error message. Defaults to None.
        """
        self.message = message
        super().__init__(message)


class PaymentOptype(Enum):
    INCOME = "income"
    DEBIT = "debit"
    REFUND = "refund"


class MoyklassApi:
    def __init__(
        self, api_key: str, base_url: str = "https://api.moyklass.com"
    ) -> None:
        """
        Initializes the MoyklassApi instance.

        Args:
            api_key (str): API key for authentication.
            base_url (str, optional): Base URL for the Moyklass API. Defaults to "https://api.moyklass.com".
        """
        self.base_url = base_url
        self.api_key = api_key
        self.token = None

    def set_token(self) -> None:
        """
        Obtains and sets the authentication token.
        """
        data = {"apiKey": self.api_key}
        r = self._make_request("POST", "v1/company/auth/getToken", data=data)
        self.token = r["accessToken"]

    def revoke_token(self) -> None:
        """
        Revokes the authentication token.
        """
        self._make_request("POST", "v1/company/auth/revokeToken")
        self.token = None

    def _make_request(
        self,
        method: str,
        path: str,
        data: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
    ) -> Dict[str, Any] | str:
        """
        Makes a request to the Moyklass API.

        Args:
            method (str): HTTP method (e.g., "GET", "POST").
            path (str): API endpoint path.
            data (Dict[str, Any], optional): Request body data. Defaults to None.
            params (Dict[str, Any], optional): Query parameters. Defaults to None.

        Returns:
            Union[Dict[str, Any], str]: Response data or response text if JSON decoding fails.
        """
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
        except requests.TooManyRedirects as err:
            raise MoyklassApiException(f"Too many redirects: {err}")
        except requests.HTTPError as err:
            raise MoyklassApiException(f"HTTPError occurred: {err}")
        except requests.Timeout as err:
            raise MoyklassApiException(f"Timeout error: {err}")
        except requests.ConnectionError as err:
            raise MoyklassApiException(f"Connection is lost, try again later: {err}")
        except requests.exceptions.RequestException as err:
            raise MoyklassApiException(f"Some error occurred: {err}")

        logging.debug(f"Response: {r.status_code}, {r.content}")

        try:
            response_data = r.json()
        except requests.JSONDecodeError:
            response_data = r.text

        return response_data

    def __enter__(self) -> "MoyklassApi":
        """
        Sets the authentication token when entering a context manager block.

        Returns:
            MoyklassApi: The current instance.
        """
        self.set_token()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Revokes the authentication token when exiting a context manager block.
        """
        self.revoke_token()

    def get_payments(
        self,
        created_at: List[str] | None = None,
        date: List[str] | None = None,
        summa: List[int] | None = None,
        invoice_id: int | None = None,
        optype: List[PaymentOptype] | None = None,
        payment_type_id: int | None = None,
        include_user_subscriptions: bool | None = False,
        user_id: int | None = None,
        filial_id: List[int] | None = None,
        append_invoices: bool | None = False,
        offset: int = 0,
        limit: int = 100,
    ) -> Dict[str, Any]:
        """
        Retrieves payment information from the Moyklass API.

        Args:
            created_at (List[str], optional): List of creation dates. Defaults to None.
            date (List[str], optional): List of payment dates. Defaults to None.
            summa (List[int], optional): List of payment amounts. Defaults to None.
            invoice_id (int, optional): Invoice ID. Defaults to None.
            optype (List[PaymentOptype], optional): List of payment operation types. Defaults to None.
            payment_type_id (int, optional): Payment type ID. Defaults to None.
            include_user_subscriptions (bool, optional): Include user subscriptions in the response. Defaults to False.
            user_id (int, optional): User ID. Defaults to None.
            filial_id (List[int], optional): List of filial IDs. Defaults to None.
            append_invoices (bool, optional): Append invoices to the response. Defaults to False.
            offset (int, optional): Offset for pagination. Defaults to 0.
            limit (int, optional): Limit for pagination. Defaults to 100.

        Returns:
            Dict[str, Any]: Response data from the Moyklass API.

        Note:
            https://api.moyklass.com/#tag/payments/paths/~1v1~1company~1payments/get
        """
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
            decoded_optype = [
                el.value for el in optype if isinstance(el, PaymentOptype)
            ]
            if decoded_optype:
                params["optype"] = decoded_optype

        if payment_type_id is not None:
            params["paymentTypeId"] = payment_type_id

        params["includeUserSubscriptions"] = str(include_user_subscriptions).lower()

        if user_id is not None:
            params["userId"] = user_id

        if filial_id is not None:
            params["filialId"] = filial_id

        params["appendInvoices"] = str(append_invoices).lower()

        params["offset"] = offset
        params["limit"] = limit

        return self._make_request("GET", "v1/company/payments", params=params)

    def get_user(self, user_id: int) -> Dict[str, Any]:
        """
        Retrieves user information from the Moyklass API.

        Args
            user_id (int): The unique identifier for the user whose information is to be retrieved.

        Returns:
            Dict[str, Any]: A dictionary containing user information retrieved from the Moyklass API.

        Note:
            https://api.moyklass.com/#tag/users/paths/~1v1~1company~1users~1%7BuserId%7D/get
        """
        path = f"v1/company/users/{user_id}"
        return self._make_request("GET", path)
