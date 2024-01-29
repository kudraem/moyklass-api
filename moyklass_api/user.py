from enum import Enum
from typing import Any, Dict, List

from moyklass_api.client import MoyklassApi


class UserSort(Enum):
    ID = "id"
    NAME = "name"
    CREATED_AT = "createdAt"
    UPDATED_AT = "updatedAt"


class UserSortDirection(Enum):
    ASC = "asc"
    DESC = "desc"


class User:
    def __init__(self, client: "MoyklassApi") -> None:
        self.client = client

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
        return self.client._make_request("GET", path)

    def get_users(
        self,
        created_at: List[str] | None = None,
        updated_at: List[str] | None = None,
        state_change_at: List[str] | None = None,
        phone: str | None = None,
        email: str | None = None,
        name: str | None = None,
        offset: int = 0,
        limit: int = 100,
        sort: UserSort = UserSort.ID,
        sort_direction: UserSortDirection = UserSortDirection.ASC,
        amoCRM_contact_id: int | None = None,
        bitrix24_contact_id: int | None = None,
        include_pay_link: bool = False,
    ):
        params = {}
        if created_at is not None:
            params["createdAt"] = created_at

        if updated_at is not None:
            params["updatedAt"] = updated_at

        if state_change_at is not None:
            params["stateChangeAt"] = state_change_at

        if phone is not None:
            params["phone"] = phone

        if email is not None:
            params["email"] = email

        if name is not None:
            params["name"] = name

        params["offset"] = offset
        params["limit"] = limit

        if isinstance(sort, UserSort):
            params["sort"] = sort.value

        if isinstance(sort_direction, UserSortDirection):
            params["sortDirection"] = sort_direction.value

        if amoCRM_contact_id is not None:
            params["amoCRMContactId"] = amoCRM_contact_id

        if bitrix24_contact_id is not None:
            params["bitrixContactId"] = bitrix24_contact_id

        params["includePayLink"] = str(include_pay_link).lower()

        return self.client._make_request("GET", "v1/company/users", params=params)
