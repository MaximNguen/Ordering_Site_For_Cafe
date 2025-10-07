from django.shortcuts import render, get_object_or_404
from .models import Category, Dish
from django.core.cache import cache

def menuPage(request):
    key = "menuItems"
    queryset = cache.get(key)
    if queryset is not None:
        print("GOt cache")
        return render(request, 'menu/menu.html', {'menu': queryset})

    menuItems = Category.objects.all()
    cache.set(key, menuItems, timeout=60*15)
    return render(request, 'menu/menu.html', {'menu': menuItems})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    dishes = category.dishes.all()  
    
    data = {
        'category': category,
        'dishes': dishes,
    }
    
    return render(request, 'products/category.html', data)

def product_detail(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Dish, slug=product_slug)
    
    data = {
        'category': category,
        'product': product,
    }
    
    return render(request, 'products/detail.html', data)
