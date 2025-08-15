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

def product_detail(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Dish, slug=product_slug)
    
    data = {
        'category': category,
        'product': product,
    }
    
    return render(request, 'products/detail.html', data)
