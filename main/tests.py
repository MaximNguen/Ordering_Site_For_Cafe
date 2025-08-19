import pytest
from django.urls import reverse
from django.test import Client
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


