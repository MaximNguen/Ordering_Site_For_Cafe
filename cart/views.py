from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from products.models import Dish
from .utils import add_to_cart, remove_from_cart, get_cart_items, get_cart_total, clear_cart
from .models import CartItem

@login_required
def cart_detail(request):
    cart_items = get_cart_items(request)
    total = get_cart_total(request)
    return render(request, 'cart/cart_detail.html', {'cart_items': cart_items, 'total': total})

@require_POST
@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Dish, id = product_id)
    quantity = int(request.POST.get('quantity', 1))
    mode = request.POST.get('mode', 'add')
    redirect_to = request.POST.get('next') or request.META.get('HTTP_REFERER')

    if mode == 'set':
        from .utils import get_or_create_cart
        cart = get_or_create_cart(request)
        if cart is None:
            return redirect(redirect_to or 'cart:cart_detail')
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 0})
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    else:
        add_to_cart(request, product.id, quantity)
    return redirect(redirect_to or 'cart:cart_detail')

@login_required
def cart_remove(request, product_id):
    product = get_object_or_404(Dish, id=product_id)
    remove_from_cart(request, product.id)
    return redirect('cart:cart_detail')

@login_required
def cart_clear(request):
    clear_cart(request)
    return redirect('cart:cart_detail')