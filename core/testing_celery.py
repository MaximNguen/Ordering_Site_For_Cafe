# test_report.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from orders.tasks import send_daily_sales_report

if __name__ == "__main__":
    print("🧪 Тестируем отправку отчета...")
    result = send_daily_sales_report()
    print(f"📋 Результат: {result}")