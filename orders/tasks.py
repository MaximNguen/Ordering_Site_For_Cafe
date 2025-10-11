# orders/tasks.py
import os

from celery import shared_task
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
import requests
import json


@shared_task
def send_daily_sales_report():
    """
    Отправляет ежедневный отчет по продажам через бота
    """
    from .models import Order, OrderItem

    # Получаем даты для отчета (вчерашний день)
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)

    # Статистика за вчерашний день
    orders_yesterday = Order.objects.filter(
        created_at__date=yesterday,
        status__in=['paid', 'confirmed', 'completed']
    )

    total_orders = orders_yesterday.count()
    total_revenue = orders_yesterday.aggregate(Sum('total_price'))['total_price__sum'] or 0

    # Статистика по способам доставки
    delivery_stats = orders_yesterday.values('delivery_method').annotate(
        count=Count('id'),
        revenue=Sum('total_price')
    )

    # Статистика по способам оплаты
    payment_stats = orders_yesterday.values('payment_method').annotate(
        count=Count('id'),
        revenue=Sum('total_price')
    )

    # Топ товаров
    top_products = OrderItem.objects.filter(
        order__created_at__date=yesterday,
        order__status__in=['paid', 'confirmed', 'completed']
    ).values(
        'product__name'
    ).annotate(
        quantity=Sum('quantity'),
        revenue=Sum('price')
    ).order_by('-quantity')[:10]

    # Формируем сообщение отчета
    report_lines = [
        f"📊 <b>Ежедневный отчет по продажам</b>",
        f"📅 <i>За {yesterday.strftime('%d.%m.%Y')}</i>",
        "",
        f"📦 <b>Всего заказов:</b> {total_orders}",
        f"💰 <b>Общая выручка:</b> {total_revenue:.2f}₽",
        "",
        "<b>📦 По способам доставки:</b>"
    ]

    for stat in delivery_stats:
        method = dict(Order.DELIVERY_METHOD_CHOICES).get(stat['delivery_method'], stat['delivery_method'])
        report_lines.append(f"  • {method}: {stat['count']} зак. ({stat['revenue'] or 0:.2f}₽)")

    report_lines.extend([
        "",
        "<b>💳 По способам оплаты:</b>"
    ])

    for stat in payment_stats:
        method = dict(Order.PAYMENT_METHOD_CHOICES).get(stat['payment_method'], stat['payment_method'])
        report_lines.append(f"  • {method}: {stat['count']} зак. ({stat['revenue'] or 0:.2f}₽)")

    if top_products:
        report_lines.extend([
            "",
            "<b>🏆 Топ товаров:</b>"
        ])
        for i, product in enumerate(top_products, 1):
            report_lines.append(
                f"  {i}. {product['product__name']}: {product['quantity']} шт. ({product['revenue'] or 0:.2f}₽)")

    report_text = "\n".join(report_lines)

    # Отправляем отчет через бота
    try:
        payload = {
            "chat_id": settings.TELEGRAM_ADMIN_CHAT_ID,
            "text": report_text,
            "parse_mode": "HTML"
        }

        # Используем прямой вызов Telegram API
        bot_token = os.getenv("BOT_TOKEN")
        if bot_token:
            response = requests.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                json=payload,
                timeout=10
            )
            print(f"Отчет отправлен: {response.status_code}")
        else:
            print("BOT_TOKEN не настроен")

    except Exception as e:
        print(f"Ошибка отправки отчета: {e}")

    return f"Отчет отправлен за {yesterday}"