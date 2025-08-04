from django.shortcuts import render
from CompanyText import Texts
from .models import Category, Promotions

def home(request):
    menuItems = Category.objects.all()
    promoItems = Promotions.objects.all()

    data = {"title": Texts.title, "menu": menuItems, "promotions": promoItems}
    return render(request, 'home.html', context=data)
