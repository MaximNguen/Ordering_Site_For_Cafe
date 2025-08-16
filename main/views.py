from django.shortcuts import render
from CompanyText import Texts
from .models import Category, Promotions, Vacancy
from products import models

def home(request):
    menuItems = Category.objects.all()
    promoItems = Promotions.objects.all()
    slugs = models.Category.objects.all()

    data = {"title": Texts.title, "menu": menuItems, "promotions": promoItems, 'slugs': slugs}
    return render(request, 'home.html', context=data)

def vacancies(request):
    vacancies = Vacancy.objects.all()

    return render(request, 'vacancy/vacancy_page.html', {"vacancies": vacancies})

def promotions(request):
    promos = Promotions.objects.all()

    return render(request, 'promotions/promo-page.html', {"promos": promos})

def conditions(request):
    return render(request, 'conditions.html')