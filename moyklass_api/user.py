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

    def create_user(
        self,
        name: str,
        email: str | None = None,
        phone: str | None = None,
        adv_source_id: int | None = None,
        create_source_id: int | None = None,
        status_change_reason_id: int | None = None,
        client_state_id: int | None = None,
        filials: List[int] | None = None,
        responsibles: List[int] | None = None,
        attributes: List[Dict[str, Any]] | None = None,
    ):
        params = {}
        params["name"] = name

        if email is not None:
            params["email"] = email

        if phone is not None:
            params["phone"] = phone

        if adv_source_id is not None:
            params["advSourceId"] = adv_source_id

        if create_source_id is not None:
            params["createSourceId"] = create_source_id

        if status_change_reason_id is not None:
            params["statusChangeReasonId"] = status_change_reason_id

        if client_state_id is not None:
            params["clientStateId"] = client_state_id

        if filials is not None:
            params["filials"] = filials

        if responsibles is not None:
            params["responsibles"] = responsibles

        if attributes is not None:
            params["attributes"] = attributes

        return self.client._make_request("POST", "v1/company/users", params=params)

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
