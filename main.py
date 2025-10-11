import os
import asyncio
import logging
from typing import Dict, Any
from datetime import datetime, timedelta

import requests
from aiohttp import web
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))
DJANGO_BASE_URL = os.getenv("DJANGO_BASE_URL")
BOT_SHARED_SECRET = os.getenv("BOT_SHARED_SECRET")
PORT = int(os.getenv("BOT_SERVICE_PORT", "8081"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bot")

if not BOT_TOKEN or not ADMIN_CHAT_ID or not DJANGO_BASE_URL:
    raise RuntimeError("BOT_TOKEN, ADMIN_CHAT_ID, DJANGO_BASE_URL must be set in .env")


bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

def build_keyboard(order_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"confirm_{order_id}"),
            InlineKeyboardButton(text="❌ Отменить", callback_data=f"cancel_{order_id}")
        ]
    ])

def order_text(data: Dict[str, Any]) -> str:
    lines = [
        f"📦 <b>Новый заказ #{data['order_id']}</b>",
        f"👤 Имя - {data.get('first_name') or '—'}",
        f"📞 Номер телефона - {data.get('phone') or '—'}",
        f"💰 Способ оплаты - {data.get('payment_method')}",
    ]
    if data.get('is_paid'):
        lines.append(f"💰 Статус оплаты (Картой) - {data.get('is_paid') or '-'}")

    if data.get("pickup_address"):
        lines.append("🚚 Самовывоз")
        lines.append(f"🏠 Адрес заведения - {data.get('pickup_address') or '—'}")
    else:
        lines.append(f"🚚 {data.get('delivery_method') or '—'}")
        lines.append(f"🏠 Адрес доставки - {data.get('address') or '—'}")



    lines.append(f"💰 Итоговая сумма - <b>{data.get('total')}₽</b>")

    comment = data.get("comment")
    if comment:
        lines.append(f"📝 {comment}")

    items = data.get("items") or []
    if items:
        lines.append("")
        lines.append("💰 Заказ:")
        for it in items:
            lines.append(f"• {it['name']} x{it['qty']} = {it['total']}₽")

    return "\n".join(lines)

async def call_django_update(order_id: int, action: str) -> bool:
    url = f"{DJANGO_BASE_URL.rstrip('/')}/orders/api/bot/{order_id}/{action}/"
    headers = {"X-Api-Key": BOT_SHARED_SECRET, "Content-Type": "application/json"}

    try:
        print(f">>> [Bot] Отправка в Django: {url}")
        print(f">>> [Bot] Секрет: {BOT_SHARED_SECRET}")

        r = requests.post(url, headers=headers, timeout=10)
        print(f">>> [Bot] Ответ Django: {r.status_code} {r.text}")

        return r.status_code == 200
    except Exception as e:
        logger.exception("Call to Django failed: %s", e)
        return False


async def handle_send_order(request: web.Request):
    secret = request.headers.get("X-Api-Key")
    if secret != BOT_SHARED_SECRET:
        return web.Response(status=403, text="Forbidden")

    try:
        data = await request.json()
    except Exception:
        return web.Response(status=400, text="Bad JSON")

    try:
        text = order_text(data)
        kb = build_keyboard(int(data["order_id"]))
        await bot.send_message(chat_id=ADMIN_CHAT_ID, text=text, reply_markup=kb)
    except Exception as e:
        logger.exception("Failed to send message: %s", e)
        return web.Response(status=500, text=str(e))

    return web.Response(text="ok")

@dp.callback_query(F.data.startswith("confirm_"))
async def on_confirm(callback: types.CallbackQuery):
    order_id = int(callback.data.split("_", 1)[1])
    ok = await call_django_update(order_id, "confirm")
    if ok:
        await callback.answer("Заказ подтверждён")
        try:
            await callback.message.edit_text(callback.message.html_text + "\n\n✅ Подтверждён")
        except Exception:
            await callback.message.answer("✅ Заказ подтверждён")
    else:
        await callback.answer("Ошибка обновления статуса", show_alert=True)

@dp.callback_query(F.data.startswith("cancel_"))
async def on_cancel(callback: types.CallbackQuery):
    order_id = int(callback.data.split("_", 1)[1])
    ok = await call_django_update(order_id, "cancel")
    if ok:
        await callback.answer("Заказ отменён")
        try:
            await callback.message.edit_text(callback.message.html_text + "\n\n❌ Отменён")
        except Exception:
            await callback.message.answer("❌ Заказ отменён")
    else:
        await callback.answer("Ошибка обновления статуса", show_alert=True)

@dp.message()
async def fallback(msg: types.Message):
    await msg.answer("Я служебный бот. Заказы присылает сайт автоматически.")


@dp.message(F.text == "/report")
async def send_manual_report(message: types.Message):
    """Ручная отправка отчета по продажам"""
    if message.from_user.id != ADMIN_CHAT_ID:
        await message.answer("У вас нет прав для этой команды")
        return

    from orders.tasks import send_daily_sales_report
    try:
        result = send_daily_sales_report.delay()
        await message.answer("Отчет запущен...")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

async def start_http_server():
    app = web.Application()
    app.router.add_post("/send_order", handle_send_order)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    logger.info(f"HTTP server started at http://0.0.0.0:{PORT}")

async def main():
    await start_http_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
