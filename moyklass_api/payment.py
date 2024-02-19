from enum import Enum
from typing import Any, Dict, List

from moyklass_api.client import MoyklassApi


class PaymentOptype(Enum):
    INCOME = "income"
    DEBIT = "debit"
    REFUND = "refund"


class Payment:
    def __init__(self, client: "MoyklassApi") -> None:
        self.client = client

    def get_payments(
        self,
        created_at: List[str] | None = None,
        date: List[str] | None = None,
        summa: List[int] | None = None,
        invoice_id: int | None = None,
        optype: List[PaymentOptype] | None = None,
        payment_type_id: int | None = None,
        include_user_subscriptions: bool = False,
        user_id: int | None = None,
        filial_id: List[int] | None = None,
        append_invoices: bool = False,
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
            include_user_subscriptions (bool): Include user subscriptions in the response. Defaults to False.
            user_id (int, optional): User ID. Defaults to None.
            filial_id (List[int], optional): List of filial IDs. Defaults to None.
            append_invoices (bool): Append invoices to the response. Defaults to False.
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

        return self.client._make_request("GET", "v1/company/payments", params=params)

    def get_payment_types(self) -> List[Dict[str, Any]]:
        """
        Retrieves a list of payment types from the Moyklass API.

        Returns:
            List[Dict[str, Any]]: A list containing dictionaries of payment types.

        Note:
            https://api.moyklass.com/#tag/catalog/paths/~1v1~1company~1paymentTypes/get
        """
        return self.client._make_request("GET", "v1/company/paymentTypes")

    def create_payments(
        self,
        user_id: int,
        date: str,
        summa: float,
        optype: PaymentOptype,
        payment_type_id: int,
        user_subscription_id: int | None = None,
        filial_id: int | None = None,
        comment: str | None = None,
        manager_id: int | None = None,
        cashbox_id: int | None = None,
    ) -> Dict[str, Any]:
        """
        Creates a new payment.

        Args:
            user_id (int): The ID of the user associated with the payment.
            date (str): The date of the payment.
            summa (float): The amount of the payment.
            optype (PaymentOptype): The type of operation for the payment.
            payment_type_id (int): The ID of the payment type.
            user_subscription_id (int, optional): The ID of the user subscription associated with the payment. Defaults to None.
            filial_id (int, optional): The ID of the filial associated with the payment. Defaults to None.
            comment (str, optional): A comment associated with the payment. Defaults to None.
            manager_id (int, optional): The ID of the manager associated with the payment. Defaults to None.
            cashbox_id (int, optional): The ID of the cashbox associated with the payment. Defaults to None.

        Returns:
            Dict[str, Any]: A dictionary containing the response from the Moyklass API.
        Note:
            https://api.moyklass.com/#tag/payments/paths/~1v1~1company~1payments/post
        """
        data = {}
        data["userId"] = user_id
        data["date"] = date
        data["summa"] = summa

        if isinstance(optype, PaymentOptype):
            data["optype"] = optype.value

        data["paymentTypeId"] = payment_type_id

        if user_subscription_id is not None:
            data["userSubscriptionId"] = user_subscription_id

        if filial_id is not None:
            data["filialId"] = filial_id

        if comment is not None:
            data["comment"] = comment

        if manager_id is not None:
            data["managerId"] = manager_id

        if cashbox_id is not None:
            data["cashboxId"] = cashbox_id

        return self.client._make_request("POST", "v1/company/payments", data=data)
