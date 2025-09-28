import pytest
from django.contrib.auth.models import User
from products.models import Category, Dish
from cart.models import Cart
from orders.models import Order
import factory
from factory.django import DjangoModelFactory, ImageField

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{str(n)}')
    email = factory.Sequence(lambda n: f'user{str(n)}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'testpassword123')

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f'Category {str(n)}')
    description = factory.Faker('text')
    slug = factory.Sequence(lambda n: f'category-{n}')


class DishFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Dish

    name = factory.Sequence(lambda n: f'Dish {n}')
    category = factory.SubFactory(CategoryFactory)
    description = factory.Faker('text')
    price = factory.Faker('random_int', min=100, max=1000)
    is_available = True
    image = ImageField(color='red')
    slug = factory.Sequence(lambda n: f'dish-{n}')


@pytest.fixture
def user():
    return UserFactory()

@pytest.fixture
def category():
    return CategoryFactory()

@pytest.fixture
def dish(category):
    return DishFactory(category=category)

@pytest.fixture
def cart(user):
    return Cart.objects.create(user=user)

@pytest.fixture
def order(user, cart):
    return Order.objects.create(
        user=user,
        cart=cart,
        total_price=2000,
        payment_method='card',
        delivery_method='delivery',
        delivery_address='Test Address',
        phone_number='+1234567890'
    )