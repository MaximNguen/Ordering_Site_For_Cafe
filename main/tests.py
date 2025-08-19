import pytest
from django.urls import reverse
from django.test import Client, TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from main.models import *

@pytest.fixture
def test_image():
    return SimpleUploadedFile(
        name='logo.png',
        content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b',
        content_type='image/png'
    )

@pytest.fixture
def category(test_image):
    return Category.objects.create(
        name='test',
        image=test_image,
        slug = 'test'
    )

@pytest.fixture
def promotion(test_image):
    return Promotions.objects.create(
        name="Скидка 20%",
        redText="Только сегодня!",
        time_type="Акция недели",
        description="Скидка на все супы",
        image=test_image,
        slug="discount-20"
    )

@pytest.fixture
def vacancy():
    return Vacancy.objects.create(
        name="Повар",
        time_type="Полная занятость",
        salary=40000,
        description="Требуется опытный повар"
    )

@pytest.fixture
def client():
    return Client()

@pytest.mark.django_db
def test_category_model(category):
    assert category.name == 'test'
    assert category.slug == 'test'

def TestContentView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.category = Category.objects.create(name="Напитки", slug="drinks")
        cls.promotion = Promotions.objects.create(name="Акция", redText="Скидка")

    def test_homepage_menu_cards(self):
        response = self.client.get(reverse('main:index'))
        self.assertEqual(response.status_code == 200)
        self.assertContains(response, '<section class="menu-section">')
        self.assertContains(response, self.category.name)
        self.assertContains(response, f'href="/menu/{self.category.slug}/"')


