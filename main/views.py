from django.shortcuts import render
from CompanyText import Texts
from .models import Category, Promotions, Vacancy
from products import models
from django.views.decorators.cache import cache_page

@cache_page(60*15)
def home(request):
    menuItems = Category.objects.all()
    promoItems = Promotions.objects.all()
    slugs = models.Category.objects.all()

    data = {"title": Texts.title, "menu": menuItems, "promotions": promoItems, 'slugs': slugs}
    return render(request, 'home.html', context=data)


@cache_page(60*15)
def vacancies(request):
    vacancies = Vacancy.objects.all()

    return render(request, 'vacancy/vacancy_page.html', {"vacancies": vacancies})

@cache_page(60*15)
def promotions(request):
    promos = Promotions.objects.all()

    return render(request, 'promotions/promo-page.html', {"promos": promos})

@cache_page(60*15)
def conditions(request):
    return render(request, 'conditions.html')