from typing import Any, Dict, List

from moyklass_api.client import MoyklassApi


class Task:
    def __init__(self, client: "MoyklassApi") -> None:
        self.client = client

    def create_task(
        self,
        body: str,
        begin_date: str,
        end_date: str,
        is_all_day: bool = False,
        is_complete: bool = False,
        reminds: List[int] | None = None,
        manager_ids: List[int] | None = None,
        user_id: int | None = None,
        owner_id: int | None = None,
        class_ids: List[int] | None = None,
        filial_ids: List[int] | None = None,
        category_id: int | None = None,
    ) -> Dict[str, Any]:
        """
        Adds a new task.

        Args:
            body (str): The description or content of the task.
            begin_date (str): The start date of the task.
            end_date (str): The end date of the task.
            is_all_day (bool, optional): Indicates if the task is an all-day event. Defaults to False.
            is_complete (bool, optional): Indicates if the task is complete. Defaults to False.
            reminds (List[int], optional): List of reminder IDs. Defaults to None.
            manager_ids (List[int], optional): List of manager IDs associated with the task. Defaults to None.
            user_id (int, optional): The ID of the user associated with the task. Defaults to None.
            owner_id (int, optional): The ID of the owner associated with the task. Defaults to None.
            class_ids (List[int], optional): List of class IDs associated with the task. Defaults to None.
            filial_ids (List[int], optional): List of filial IDs associated with the task. Defaults to None.
            category_id (int, optional): The ID of the category associated with the task. Defaults to None.

        Returns:
            Dict[str, Any]: A dictionary containing the response from the Moyklass API.

        Note:
            https://api.moyklass.com/#tag/tasks/paths/~1v1~1company~1tasks/post
        """
        data = {}
        data["body"] = body
        data["beginDate"] = begin_date
        data["endDate"] = end_date
        data["isAllDay"] = is_all_day
        data["isComplete"] = is_complete

        if reminds is not None:
            data["reminds"] = reminds

        if manager_ids is not None:
            data["managerIds"] = manager_ids

        if user_id is not None:
            data["userId"] = user_id

        if owner_id is not None:
            data["ownerId"] = owner_id

        if class_ids is not None:
            data["classIds"] = class_ids

        if filial_ids is not None:
            data["filialIds"] = filial_ids

        if category_id is not None:
            data["categoryId"] = category_id

        return self.client._make_request("POST", "v1/company/tasks", data=data)
