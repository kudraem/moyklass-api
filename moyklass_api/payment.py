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
