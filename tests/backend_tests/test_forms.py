import pytest
from accounts.forms import SignUpForm, LoginForm
from orders.forms import OrderForm

@pytest.mark.django_db
def test_signup_form_valid():
    form_data = {
        'first_name': 'Test',
        'last_name': 'User',
        'username': 'testuser',
        'email': 'test@example.com',
        'password1': 'testpassword123',
        'password2': 'testpassword123'
    }
    form = SignUpForm(data=form_data)
    assert form.is_valid()

@pytest.mark.django_db
def test_order_form_delivery():
    form_data = {
        'delivery_method': 'delivery',
        'payment_method': 'card',
        'delivery_address': 'Test Address',
        'phone_number': '+1234567890'
    }
    form = OrderForm(data=form_data)
    assert form.is_valid()

@pytest.mark.django_db
def test_order_form_pickup():
    form_data = {
        'delivery_method': 'pickup',
        'payment_method': 'afterpay',
        'phone_number': '+1234567890'
    }
    form = OrderForm(data=form_data)
    assert not form.is_valid()