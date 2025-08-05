from django.shortcuts import render, get_object_or_404
from .models import Category, Dish

def menuPage(request):
    menuItems = Category.objects.all()

    return render(request, 'menu/menu.html', {'menu': menuItems})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    dishes = category.dishes.all()  
    
    data = {
        'category': category,
        'dishes': dishes,
    }
    
    return render(request, 'products/category.html', data)