import sys

from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve
from main.models import Category, Promotions, Vacancy
from django.core.files.uploadedfile import SimpleUploadedFile

class MainViewTest(SimpleTestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view(self):
        response = self.client.get(reverse('main:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertIn('menu', response.context)
        self.assertIn('promotions', response.context)

    def test_vacancies_view(self):
        response = self.client.get(reverse('main:vacancies'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vacancy/vacancy_page.html')
        self.assertIn('vacancies', response.context)

    def test_promotions_view(self):
        response = self.client.get(reverse('main:promo'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'promotions/promo-page.html')
        self.assertIn('promos', response.context)

    def test_conditions_view(self):
        response = self.client.get(reverse('main:conditions'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conditions.html')

    def test_empty_views(self):
        response = self.client.get(reverse('main:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['menu']), [])

        response = self.client.get(reverse('main:vacancies'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['vacancies']), [])

class ContentDisplayTest(SimpleTestCase):
    def setUp(self):
        self.client = Client()

    def test_homepage_menu_cards(self):
        response = self.client.get(reverse('main:index'))
        self.assertContains(response, 'Меню')

    def test_promotions_display(self):
        response = self.client.get(reverse('main:index'))
        self.assertContains(response, 'Акция')

    def test_main_navigation(self):
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()

        self.assertIn('Главная', content)
        self.assertIn('Акция', content)
        self.assertIn('Меню', content)
        self.assertIn('Вакансии', content)

    def test_footer_content(self):
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()

        self.assertIn('О нас', content)
        self.assertIn('+7 (123) 456-78-90', content)
        self.assertIn('info@cafe.ru', content)
        self.assertIn('Пн-Вс: 9:00 - 23:00', content)

    def test_conditions_page(self):
        response = self.client.get(reverse('main:conditions'))
        content = response.content.decode()

        self.assertIn('Условия доставки и самовызова', content)
        self.assertIn('предоплату на нетипичные заказы', content)

    def test_empty_promotions(self):
        Promotions.objects.all().delete()
        response = self.client.get(reverse('main:promo'))
        self.assertContains(response, 'у нас нет акций')

    def test_empty_vacancies(self):
        Vacancy.objects.all().delete()
        response = self.client.get(reverse('main:vacancies'))
        self.assertContains(response, 'нет открытых вакансий')
