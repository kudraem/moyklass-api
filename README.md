# Пакет для работы с API CRM moyklass.com

> [!WARNING]  
> Пакет не рекомендуется к использованию, т.к. не покрыт тестами и находится на стадии разработки 

## Пример с использованием менеджера контекста
```python
from moyklass_api.client import MoyklassApi
from moyklass_api.payment import Payment

api_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
with MoyklassApi(api_key) as mc:
    mc_payment = Payment(mc)
    try:
        payments = mc_payment.get_payments(date=["2024-01-24", "2024-01-24"])
    except Exception:
        print("Возникла ошибка при получении оплат")
    else:
        for p in payments["payments"]:
            print(p["id"], p["summa"])
```

## Пример без использования менеджера контекста
```python
from moyklass_api.client import MoyklassApi
from moyklass_api.payment import Payment

api_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
mc = MoyklassApi(api_key)
mc.set_token()

mc_payment = Payment(mc)
try:
    payments = mc_payment.get_payments(date=["2024-01-24", "2024-01-24"])
except Exception:
    print("Возникла ошибка при получении оплат")
else:
    for p in payments["payments"]:
        print(p["id"], p["summa"])

mc.revoke_token()
```

## Пример с использованием логирования
```python
import logging

from moyklass_api.client import MoyklassApi
from moyklass_api.payment import Payment

logging.basicConfig(
    format="%(asctime)s:%(levelname)s:%(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.DEBUG,
)

api_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
with MoyklassApi(api_key) as mc:
    mc_payment = Payment(mc)
    try:
        payments = mc_payment.get_payments(date=["2024-01-24", "2024-01-24"])
    except Exception:
        print("Возникла ошибка при получении оплат")
    else:
        for p in payments["payments"]:
            print(p["id"], p["summa"])
```