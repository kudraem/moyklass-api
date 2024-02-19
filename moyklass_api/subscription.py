from typing import Any, Dict

from moyklass_api.client import MoyklassApi


class Subscription:
    def __init__(self, client: "MoyklassApi") -> None:
        self.client = client

    def get_subscription(self, subscription_id: int) -> Dict[str, Any]:
        """
        Retrieves information about a specific subscription.

        Args:
            subscription_id (int): The ID of the subscription.

        Returns:
            Dict[str, Any]: A dictionary containing subscription information.

        Note:
            https://api.moyklass.com/#tag/subscriptions/paths/~1v1~1company~1subscriptions~1%7BsubscriptionId%7D/get
        """
        path = f"v1/company/subscriptions/{subscription_id}"
        return self.client._make_request("GET", path)

    def get_groupings(self, include_subscriptions: bool = False) -> Dict[str, Any]:
        """
        Retrieves subscription groupings.

        Args:
            include_subscriptions (bool, optional): Whether to include subscriptions. Defaults to False.

        Returns:
            Dict[str, Any]: A dictionary containing subscription groupings.

        Note:
            https://api.moyklass.com/#tag/subscriptions/paths/~1v1~1company~1subscriptionGroupings/get
        """
        params = {}
        params["includeSubscriptions"] = str(include_subscriptions).lower()
        return self.client._make_request(
            "GET", "v1/company/subscriptionGroupings", params=params
        )
