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


class UserSubscriptionId(Enum):
    NOT_ACTIVE = 1
    ACTIVE = 2
    FROZEN = 3
    FINISHED = 4


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
    ) -> Dict[str, Any]:
        """
        Creates a new user using the provided information.

        Args:
            name (str): The name of the user.
            email (str, optional): The email address of the user. Defaults to None.
            phone (str, optional): The phone number of the user. Defaults to None.
            adv_source_id (int, optional): The advertisement source ID. Defaults to None.
            create_source_id (int, optional): The creation source ID. Defaults to None.
            status_change_reason_id (int, optional): The status change reason ID. Defaults to None.
            client_state_id (int, optional): The client state ID. Defaults to None.
            filials (List[int], optional): List of filial IDs. Defaults to None.
            responsibles (List[int], optional): List of responsible user IDs. Defaults to None.
            attributes (List[Dict[str, Any]], optional): List of attribute dictionaries. Defaults to None.

        Returns:
            Dict[str, Any]: A dictionary containing the response from the Moyklass API.

        Note:
            https://api.moyklass.com/#tag/users/paths/~1v1~1company~1users/post
        """
        data = {}
        data["name"] = name

        if email is not None:
            data["email"] = email

        if phone is not None:
            data["phone"] = phone

        if adv_source_id is not None:
            data["advSourceId"] = adv_source_id

        if create_source_id is not None:
            data["createSourceId"] = create_source_id

        if status_change_reason_id is not None:
            data["statusChangeReasonId"] = status_change_reason_id

        if client_state_id is not None:
            data["clientStateId"] = client_state_id

        if filials is not None:
            data["filials"] = filials

        if responsibles is not None:
            data["responsibles"] = responsibles

        if attributes is not None:
            data["attributes"] = attributes

        return self.client._make_request("POST", "v1/company/users", data=data)

    def update_user(
        self,
        user_id: int,
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
    ) -> Dict[str, Any]:
        """
        Updates the information of an existing user.

        Args:
            user_id (int): The ID of the user to update.
            name (str): The updated name of the user.
            email (str, optional): The updated email address of the user. Defaults to None.
            phone (str, optional): The updated phone number of the user. Defaults to None.
            adv_source_id (int, optional): The updated advertisement source ID. Defaults to None.
            create_source_id (int, optional): The updated creation source ID. Defaults to None.
            status_change_reason_id (int, optional): The updated status change reason ID. Defaults to None.
            client_state_id (int, optional): The updated client state ID. Defaults to None.
            filials (List[int], optional): Updated list of filial IDs. Defaults to None.
            responsibles (List[int], optional): Updated list of responsible user IDs. Defaults to None.
            attributes (List[Dict[str, Any]], optional): Updated list of attribute dictionaries. Defaults to None.

        Returns:
            Dict[str, Any]: A dictionary containing the response from the Moyklass API.
        Note:
            https://api.moyklass.com/#tag/users/paths/~1v1~1company~1users~1%7BuserId%7D/post
        """
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

        return self.client._make_request(
            "POST", f"v1/company/users/{user_id}", params=params
        )

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
    ) -> Dict[str, Any]:
        """
        Retrieves a list of users based on specified filters.

        Args:
            created_at (List[str], optional): List of creation dates. Defaults to None.
            updated_at (List[str], optional): List of update dates. Defaults to None.
            state_change_at (List[str], optional): List of state change dates. Defaults to None.
            phone (str, optional): Phone number filter. Defaults to None.
            email (str, optional): Email filter. Defaults to None.
            name (str, optional): Name filter. Defaults to None.
            offset (int, optional): Result offset for pagination. Defaults to 0.
            limit (int, optional): Maximum number of results to return. Defaults to 100.
            sort (UserSort, optional): Sort parameter. Defaults to UserSort.ID.
            sort_direction (UserSortDirection, optional): Sort direction parameter. Defaults to UserSortDirection.ASC.
            amoCRM_contact_id (int, optional): amoCRM contact ID filter. Defaults to None.
            bitrix24_contact_id (int, optional): Bitrix24 contact ID filter. Defaults to None.
            include_pay_link (bool, optional): Whether to include pay link. Defaults to False.

        Returns:
            Dict[str, Any]: A dictionary containing the response from the Moyklass API.

        Note:
            https://api.moyklass.com/#tag/users/paths/~1v1~1company~1users/get
        """
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

    def get_user_attributes(self) -> Dict[str, Any]:
        """
        Retrieves a list of user's attributes.

        Returns:
            Dict[str, Any]: A dictionary containing the response from the Moyklass API.

        Note:
            https://api.moyklass.com/#tag/catalog/paths/~1v1~1company~1userAttributes/get
        """
        return self.client._make_request("GET", "v1/company/userAttributes")

    def get_user_subscriptions(
        self,
        user_id: int | None = None,
        manager_id: int | None = None,
        external_id: str | List[str] | None = None,
        course_id: List[int] | None = None,
        class_id: List[int] | None = None,
        main_class_id: int | List[int] | None = None,
        sell_date: List[str] | None = None,
        begin_date: List[str] | None = None,
        end_date: List[str] | None = None,
        status_id: List[UserSubscriptionId] | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> Dict[str, Any]:
        """
        Retrieves a list of user subscriptions based on specified filters.

        Args:
            user_id (int, optional): The ID of the user whose subscriptions are to be retrieved. Defaults to None.
            manager_id (int, optional): The ID of the manager associated with the subscriptions. Defaults to None.
            external_id (str | List[str], optional): The external ID(s) associated with the subscriptions. Defaults to None.
            course_id (List[int], optional): The ID(s) of the courses associated with the subscriptions. Defaults to None.
            class_id (List[int], optional): The ID(s) of the classes associated with the subscriptions. Defaults to None.
            main_class_id (int | List[int], optional): The ID(s) of the main classes associated with the subscriptions. Defaults to None.
            sell_date (List[str], optional): The sell date(s) associated with the subscriptions. Defaults to None.
            begin_date (List[str], optional): The begin date(s) associated with the subscriptions. Defaults to None.
            end_date (List[str], optional): The end date(s) associated with the subscriptions. Defaults to None.
            status_id (List[UserSubscriptionId], optional): The status ID(s) associated with the subscriptions. Defaults to None.
            offset (int, optional): Result offset for pagination. Defaults to 0.
            limit (int, optional): Maximum number of results to return. Defaults to 100.

        Returns:
            Dict[str, Any]: A dictionary containing the response from the Moyklass API.

        Note:
            https://api.moyklass.com/#tag/userSubscriptions/paths/~1v1~1company~1userSubscriptions/get
        """
        params = {}

        if user_id is not None:
            params["userId"] = user_id

        if manager_id is not None:
            params["managerId"] = manager_id

        if external_id is not None:
            params["externalId"] = external_id

        if course_id is not None:
            params["courseId"] = course_id

        if class_id is not None:
            params["classId"] = class_id

        if main_class_id is not None:
            params["mainClassId"] = main_class_id

        if sell_date is not None:
            params["sellDate"] = sell_date

        if begin_date is not None:
            params["beginDate"] = begin_date

        if end_date is not None:
            params["endDate"] = end_date

        if status_id is not None:
            decoded_status_id = [
                el.value for el in status_id if isinstance(el, UserSubscriptionId)
            ]
            if decoded_status_id:
                params["statusId"] = decoded_status_id

        params["offset"] = offset
        params["limit"] = limit

        return self.client._make_request(
            "GET", "v1/company/userSubscriptions", params=params
        )

    def create_user_subscription(
        self,
        user_id: int,
        subscription_id: int,
        sell_date: str,
        class_ids: List[int],
        main_class_id: int,
        external_id: int | None = None,
        original_price: float | None = None,
        discount: float | None = None,
        extra_discount: float | None = None,
        comment: str | None = None,
        begin_date: str | None = None,
        end_date: str | None = None,
        period: str | None = None,
        visit_count: int | None = None,
        manager_id: int | None = None,
        autodebit: bool = True,
        burn_leftovers: bool = True,
        use_leftovers: bool = True,
    ) -> Dict[str, Any]:
        """
        Creates a new user subscription.

        Args:
            user_id (int): The ID of the user for whom the subscription is created.
            subscription_id (int): The ID of the subscription being assigned to the user.
            sell_date (str): The date of sale for the subscription.
            class_ids (List[int]): List of class IDs associated with the subscription.
            main_class_id (int): The ID of the main class associated with the subscription.
            external_id (int, optional): External ID for the subscription. Defaults to None.
            original_price (float, optional): The original price of the subscription. Defaults to None.
            discount (float, optional): The discount applied to the subscription. Defaults to None.
            extra_discount (float, optional): Additional discount applied to the subscription. Defaults to None.
            comment (str, optional): Additional comment for the subscription. Defaults to None.
            begin_date (str, optional): The start date of the subscription. Defaults to None.
            end_date (str, optional): The end date of the subscription. Defaults to None.
            period (str, optional): The subscription period. Defaults to None.
            visit_count (int, optional): The visit count for the subscription. Defaults to None.
            manager_id (int, optional): The ID of the manager associated with the subscription. Defaults to None.
            autodebit (bool, optional): Whether autodebit is enabled for the subscription. Defaults to True.
            burn_leftovers (bool, optional): Whether leftovers are burnt for the subscription. Defaults to True.
            use_leftovers (bool, optional): Whether leftovers are used for the subscription. Defaults to True.

        Returns:
            Dict[str, Any]: A dictionary containing the response from the Moyklass API.

        Note:
            https://api.moyklass.com/#tag/userSubscriptions/paths/~1v1~1company~1userSubscriptions/post
        """

        data = {}
        data["userId"] = user_id
        data["subscriptionId"] = subscription_id
        data["sellDate"] = sell_date
        data["classIds"] = class_ids
        data["mainClassId"] = main_class_id

        if external_id is not None:
            data["externalId"] = external_id

        if original_price is not None:
            data["originalPrice"] = original_price

        if discount is not None:
            data["discount"] = discount

        if extra_discount is not None:
            data["extraDiscount"] = extra_discount

        if comment is not None:
            data["comment"] = comment

        if begin_date is not None:
            data["beginDate"] = begin_date

        if end_date is not None:
            data["endDate"] = end_date

        if period is not None:
            data["period"] = period

        if visit_count is not None:
            data["visitCount"] = visit_count

        if manager_id is not None:
            data["managerId"] = manager_id

        data["autodebit"] = autodebit
        data["burnLeftovers"] = burn_leftovers
        data["useLeftovers"] = use_leftovers

        return self.client._make_request(
            "POST", "v1/company/userSubscriptions", data=data
        )

    def set_user_subscription_status(
        self, user_subscription_id: int, status_id: UserSubscriptionId
    ) -> Dict[str, Any]:
        """
        Sets the status of a the user subscription.

        Args:
            user_subscription_id (int): The ID of the user subscription.
            status_id (UserSubscriptionId): The status ID to set.

        Returns:
            Dict[str, Any]: A dictionary containing the response from the Moyklass API.

        Note:
            https://api.moyklass.com/#tag/userSubscriptions/paths/~1v1~1company~1userSubscriptions~1%7BuserSubscriptionId%7D~1status/post
        """
        data = {}
        if isinstance(status_id, UserSubscriptionId):
            data["statusId"] = status_id.value

        url = f"v1/company/userSubscriptions/{user_subscription_id}/status"
        return self.client._make_request("POST", url, data=data)