# Пакет для работы с API CRM moyklass.com

## Пример с использованием менеджера контекста
```python
from moyklass_api.client import MoyklassApi
from moyklass_api.payment import Payment

api_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
with MoyklassApi(api_key) as mc:
    mc_payment = Payment(mc)
    try:
        payments = mc_payment.get_payments(date=["2024-01-24", "2024-01-24"])
    except BaseException:
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
except BaseException:
    print("Возникла ошибка при получении оплат")
else:
    for p in payments["payments"]:
        print(p["id"], p["summa"])

mc.revoke_token()
```