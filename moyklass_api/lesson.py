from typing import Any, Dict, List

from moyklass_api.client import MoyklassApi


class Lesson:
    def __init__(self, client: "MoyklassApi") -> None:
        self.client = client

    def get_lessons(
        self,
        date: List[str] | None = None,
        lesson_id: List[int] | None = None,
        room_id: List[int] | None = None,
        filial_id: List[int] | None = None,
        class_id: List[int] | None = None,
        teacher_id: List[int] | None = None,
        status_id: int | None = None,
        user_id: int | None = None,
        offset: int = 0,
        limit: int = 100,
        include_records: bool = False,
        include_marks: bool = False,
        include_tasks: bool = False,
        include_task_answers: bool = False,
        include_user_subscriptions: bool = False,
        include_params: bool = False,
    ) -> Dict[str, Any]:
        """
        Retrieves a list of lessons based on specified filters.

        Args:
            date (List[str], optional): List of lesson dates. Defaults to None.
            lesson_id (List[int], optional): List of lesson IDs. Defaults to None.
            room_id (List[int], optional): List of room IDs. Defaults to None.
            filial_id (List[int], optional): List of filial IDs. Defaults to None.
            class_id (List[int], optional): List of class IDs. Defaults to None.
            teacher_id (List[int], optional): List of teacher IDs. Defaults to None.
            status_id (int, optional): Status ID. Defaults to None.
            user_id (int, optional): User ID. Defaults to None.
            offset (int, optional): Offset for pagination. Defaults to 0.
            limit (int, optional): Limit for pagination. Defaults to 100.
            include_records (bool, optional): Include records in the response. Defaults to False.
            include_marks (bool, optional): Include marks in the response. Defaults to False.
            include_tasks (bool, optional): Include tasks in the response. Defaults to False.
            include_task_answers (bool, optional): Include task answers in the response. Defaults to False.
            include_user_subscriptions (bool, optional): Include user subscriptions in the response. Defaults to False.
            include_params (bool, optional): Include parameters in the response. Defaults to False.

        Returns:
            Dict[str, Any]: A dictionary containing the response from the Moyklass API.

        Note:
            https://api.moyklass.com/#tag/lessons/paths/~1v1~1company~1lessons/get
        """
        params = {}
        if date is not None:
            params["date"] = date

        if lesson_id is not None:
            params["lessonId"] = lesson_id

        if room_id is not None:
            params["roomId"] = room_id

        if filial_id is not None:
            params["filialId"] = filial_id

        if class_id is not None:
            params["classId"] = class_id

        if teacher_id is not None:
            params["teacherId"] = teacher_id

        if status_id is not None:
            params["statusId"] = status_id

        if user_id is not None:
            params["userId"] = user_id

        params["offset"] = offset
        params["limit"] = limit
        params["include_records"] = str(include_records).lower()
        params["include_marks"] = str(include_marks).lower()
        params["include_tasks"] = str(include_tasks).lower()
        params["include_task_answers"] = str(include_task_answers).lower()
        params["include_user_subscriptions"] = str(include_user_subscriptions).lower()
        params["include_params"] = str(include_params).lower()

        return self.client._make_request("GET", "v1/company/lessons", params=params)
