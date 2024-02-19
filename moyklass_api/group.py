from typing import Any, Dict

from moyklass_api.client import MoyklassApi


class Group:
    def __init__(self, client: "MoyklassApi") -> None:
        self.client = client

    def get_courses(
        self, include_classes: bool = False, include_images: bool = False
    ) -> Dict[str, Any]:
        """
        Retrieves a list of courses.

        Returns:
            Dict[str, Any]: A dictionary containing the response from the Moyklass API.

        Note:
            https://api.moyklass.com/#tag/groups/paths/~1v1~1company~1courses/get
        """
        params = {}
        params["includeClasses"] = str(include_classes).lower()
        params["includeImages"] = str(include_images).lower()

        return self.client._make_request("GET", "v1/company/courses", params=params)

    def get_classes(
        self, include_images: bool = False, include_attributes: bool = False
    ) -> Dict[str, Any]:
        """
        Retrieves a list of groups.

        Returns:
            Dict[str, Any]: A dictionary containing the response from the Moyklass API.

        Note:
            https://api.moyklass.com/#tag/groups/paths/~1v1~1company~1classes/get
        """
        params = {}
        params["includeImages"] = str(include_images).lower()
        params["includeAttributes"] = str(include_attributes).lower()

        return self.client._make_request("GET", "v1/company/classes", params=params)
