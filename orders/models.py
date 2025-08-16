from django.db import models
from django.conf import settings
from cart.models import Cart
from delivery.models import Location
from products.models import Dish

class Order(models.Model):
    STATUS_CHOICES = (
    ('new', 'Новый'),
    ('confirmed', 'Подтвержденный'),
    ('in_progress', 'В обработке'),
    ('ready', 'Готов к выдаче'),
    ('completed', 'Завершен'),
    ('cancelled', 'Отменен'),
    )

    PAYMENT_METHOD_CHOICES = (
        ('card', 'Оплата картой'),
        ('afterpay', 'Оплата при получении'),
    )

    DELIVERY_METHOD_CHOICES = (
        ('delivery', 'Доставка'),
        ('pickup', 'Самовывоз'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='card', verbose_name='Способ оплаты')
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_METHOD_CHOICES, default='delivery', verbose_name='Способ получения')
    delivery_address = models.TextField(verbose_name='Адрес доставки')
    pickup_location = models.ForeignKey(
        Location,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Адрес заведения (для самовывоза)'
    )
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    comments = models.TextField(blank=True, null=True, verbose_name='Комментарии и время')

    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")

    def __str__(self):
        return f"Order #{self.id} - {self.user.email}"

    def get_pickup_address_display(self) -> str:
        if self.pickup_location:
            return self.pickup_location.address
        return ""


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Dish, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order #{self.order.id})"\

    def total_price(self):
        return self.price * self.quantity


