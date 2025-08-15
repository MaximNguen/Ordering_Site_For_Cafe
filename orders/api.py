import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import Order

ALLOWED_ACTIONS = {
    "confirm": "confirmed",
    "cancel": "cancelled",
}

def _check_auth(request):
    secret = request.headers.get("X-Api-Key") or request.META.get("HTTP_X_API_KEY")
    return secret and secret == settings.BOT_SHARED_SECRET

@csrf_exempt
@require_POST
def bot_update_status(request, order_id, action):
    print(f">>> [Django] Запрос от бота: order_id={order_id}, action={action}")
    if not _check_auth(request):
        print(">>> [Django] Ошибка авторизации: секрет не совпадает")
        return HttpResponseForbidden("Invalid token")

    if action not in ALLOWED_ACTIONS:
        print(f">>> [Django] Недопустимое действие: {action}")
        return HttpResponseBadRequest("Unknown action")

    order = get_object_or_404(Order, id=order_id)
    new_status = ALLOWED_ACTIONS[action]

    # Если уже в финальном статусе — не меняем
    if order.status in ("cancelled", "completed"):
        print(f">>> [Django] Заказ уже в финальном статусе: {order.status}")
        return JsonResponse({"ok": True, "status": order.status})

    order.status = new_status
    order.save(update_fields=["status"])
    print(f">>> [Django] Статус заказа #{order.id} изменён на {order.status}")

    return JsonResponse({"ok": True, "status": order.status})
