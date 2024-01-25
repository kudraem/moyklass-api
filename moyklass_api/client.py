import logging
from typing import Any, Dict

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
