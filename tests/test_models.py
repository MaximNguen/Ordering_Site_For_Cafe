import pytest
from django.test import TestCase
from products.models import Category, Dish
from orders.models import Order, OrderItem

@pytest.mark.django_db
def test_category_create():
    category = Category.objects.create(name='test', description='test', slug='test')
    assert category.slug == 'test'
    assert category.name == 'test'
    assert category.description == 'test'

@pytest.mark.django_db
def test_dish_create(category):
    dish = Dish.objects.create(name="Test Dish",
        category=category,
        description="Test Description",
        price=500,
        is_available=True,
        slug="test-dish")
    assert dish.name == 'Test Dish'
    assert dish.description == 'Test Description'
    assert dish.price == 500
    assert dish.is_available is True
    assert dish.slug == 'test-dish'

@pytest.mark.django_db
def test_order_creation(user, cart):
    order = Order.objects.create(
        user=user,
        cart=cart,
        total_price=1500,
        payment_method='card',
        delivery_method='delivery',
        delivery_address='Test Address',
        phone_number='+1234567890'
    )
    assert order.user == user
    assert order.total_price == 1500
    assert order.status == 'new'