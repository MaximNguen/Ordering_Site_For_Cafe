import pytest
from django.test import Client
from django.urls import reverse

from main.models import Vacancy
from products.models import Category, Dish

@pytest.mark.django_db
def test_home_view():
    client = Client()
    response = client.get(reverse('main:index'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_menu_view():
    client = Client()
    response = client.get(reverse('products:menuPage'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_category_detail_view(category):
    client = Client()
    response = client.get(reverse('products:category', args=[category.slug]))
    assert response.status_code == 200

@pytest.mark.django_db
def test_product_detail_view(category, dish):
    client = Client()
    response = client.get(reverse('products:product', args=[category.slug, dish.slug]))
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_order_view_authenticated(user, client):
    client.force_login(user)
    response = client.get(reverse('orders:create_order'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_order_view_unauthenticated():
    client = Client()
    response = client.get(reverse('orders:create_order'))
    assert response.status_code == 302

@pytest.mark.django_db
def test_vacancy_detail_view():
    client = Client()
    response = client.get(reverse('main:vacancies'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_conditions_view():
    client = Client()
    response = client.get(reverse('main:conditions'))
    assert response.status_code == 200