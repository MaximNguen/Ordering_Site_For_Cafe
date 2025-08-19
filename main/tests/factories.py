import factory
from main.models import Category, Promotions, Vacancy
from django.utils.text import slugify


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('word')
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
    image = factory.django.ImageField(color='blue')


class PromotionsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Promotions

    name = factory.Faker('sentence', nb_words=3)
    redText = factory.Faker('sentence', nb_words=5)
    time_type = factory.Faker('word')
    description = factory.Faker('text')
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
    image = factory.django.ImageField(color='red')


class VacancyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vacancy

    name = factory.Faker('job')
    time_type = factory.Faker('word')
    salary = factory.Faker('random_int', min=20000, max=100000)
    description = factory.Faker('text')