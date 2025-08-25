class BotNotifyError(Exception):
    pass

def send_order_to_bot(order):
    import json
    from django.conf import settings
    import requests

    items = [
        {
            "name": it.product.name,
            "qty": it.quantity,
            "price": it.price,
            "total": it.price * it.quantity,
        }
        for it in order.items.all()
    ]
    payload = {
        "order_id": order.id,
        "username": order.user.username,
        "first_name": order.user.first_name,
        "phone": order.phone_number,
        "payment_method": order.get_payment_method_display(),
        "is+paid": order.is_paid,
        "delivery_method": order.get_delivery_method_display(),
        "pickup_address": order.get_pickup_address_display(),
        "address": order.delivery_address,
        "total": str(order.total_price),
        "comment": order.comments or "",
        "items": items,
    }

    print(">>> Отправка заказа боту:", json.dumps(payload, ensure_ascii=False, indent=2))

    try:
        resp = requests.post(
            f"{settings.BOT_SERVICE_URL.rstrip('/')}/send_order",
            json=payload,
            headers={"X-Api-Key": settings.BOT_SHARED_SECRET},
            timeout=5
        )
        print(">>> Ответ бота:", resp.status_code, resp.text)
        resp.raise_for_status()
    except Exception as e:
        print(">>> Ошибка отправки заказа боту:", e)
        raise
