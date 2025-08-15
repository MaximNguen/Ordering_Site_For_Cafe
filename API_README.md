# API для интеграции с Telegram ботом

## Описание

Этот API позволяет автоматически отправлять информацию о новых заказах в Telegram бот. При создании заказа система:

1. Сохраняет данные заказа в JSON файл
2. Отправляет уведомление в Telegram бот
3. Сохраняет статус отправки в базе данных

## Установка и настройка

### 1. Установка зависимостей

```bash
pip install djangorestframework requests
```

### 2. Настройка Telegram бота

1. **Создайте бота** через @BotFather в Telegram
2. **Получите токен** бота
3. **Напишите боту** любое сообщение
4. **Получите CHAT_ID**:
   - Откройте в браузере: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Найдите `"chat":{"id": число}` - это ваш CHAT_ID

### 3. Обновите конфигурацию

Отредактируйте файл `api/telegram_config.py`:

```python
BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
CHAT_ID = "123456789"
```

### 4. Запустите миграции

```bash
python manage.py makemigrations api
python manage.py migrate
```

## Использование

### Автоматическая отправка

После настройки все новые заказы автоматически отправляются в Telegram.

### Ручная отправка

```bash
curl -X POST http://localhost:8000/api/orders/create/ \
  -H "Content-Type: application/json" \
  -d '{"order_id": 123}'
```

### Webhook

```bash
curl -X POST http://localhost:8000/api/orders/webhook/ \
  -H "Content-Type: application/json" \
  -d '{"order_id": 123}'
```

## Структура JSON файла

Заказы сохраняются в `media/orders/` в формате:

```json
{
  "id": 123,
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "Иван",
    "last_name": "Иванов"
  },
  "status": "new",
  "status_display": "Новый",
  "total_price": "1500.00",
  "payment_method": "card",
  "payment_method_display": "Оплата картой",
  "delivery_method": "delivery",
  "delivery_method_display": "Доставка",
  "delivery_address": "ул. Примерная, 123",
  "phone_number": "+79001234567",
  "comments": "Доставить до 18:00",
  "created_at": "2025-08-14T10:00:00Z",
  "items": [
    {
      "product_name": "Пицца Маргарита",
      "quantity": 2,
      "price": 500,
      "total_price": 1000
    }
  ]
}
```

## Формат сообщения в Telegram

Сообщения отправляются в формате HTML с эмодзи:

🛒 **НОВЫЙ ЗАКАЗ #123**

👤 **Клиент:** user@example.com
📱 **Телефон:** +79001234567
📍 **Способ получения:** Доставка
💳 **Способ оплаты:** Оплата картой
📅 **Дата:** 2025-08-14T10:00:00Z

📋 **Состав заказа:**
• Пицца Маргарита x2 - 1000₽

💰 **Итого: 1500.00₽**

📍 **Адрес:** ул. Примерная, 123
💬 **Комментарий:** Доставить до 18:00

## Мониторинг

В админке Django (`/admin/`) доступна таблица `TelegramNotification` для отслеживания:

- Статус отправки
- Время отправки
- Ошибки отправки

## Устранение неполадок

### Бот не отвечает
1. Проверьте токен бота
2. Убедитесь, что бот активен
3. Проверьте CHAT_ID

### Ошибки API
1. Проверьте логи Django
2. Убедитесь, что все зависимости установлены
3. Проверьте права доступа к папке `media/orders/`

### Тестирование
Для тестирования без реального бота используйте тестовые значения в `telegram_config.py`.

## Безопасность

- API доступен без аутентификации (для webhook)
- В продакшене рекомендуется добавить аутентификацию
- Проверяйте входящие данные
- Ограничьте доступ к папке с JSON файлами
