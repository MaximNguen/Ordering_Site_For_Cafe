import pytest
from django.test import Client
from orders.models import Order

@pytest.mark.django_db
def test_bot_update_status_unauthorized(user, order):
    client = Client()
    response = client.post(f'/orders/api/bot/{order.id}/confirm/')
    assert response.status_code == 403

@pytest.mark.django_db
def test_bot_update_status_invalid_action(user, order):
    client = Client()
    response = client.post(
        f'/orders/api/bot/{order.id}/invalid_action/',
        HTTP_X_API_KEY='invalid_secret'
    )
    assert response.status_code == 403