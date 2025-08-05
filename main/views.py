from django.shortcuts import render
from CompanyText import Texts
from .models import Category, Promotions
from products import models

def home(request):
    menuItems = Category.objects.all()
    promoItems = Promotions.objects.all()
    slugs = models.Category.objects.all()

    data = {"title": Texts.title, "menu": menuItems, "promotions": promoItems, 'slugs': slugs}
    return render(request, 'home.html', context=data)
