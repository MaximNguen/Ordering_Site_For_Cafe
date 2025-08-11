from .models import Cart, CartItem
from django.conf import settings

def get_or_create_cart(request):
    if not getattr(request.user, 'is_authenticated', False):
        return None
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return cart

def add_to_cart(request, product_id, quantity=1):
    from products.models import Dish
    if not getattr(request.user, 'is_authenticated', False):
        return None
    product = Dish.objects.get(id=product_id)
    cart = get_or_create_cart(request)
    if cart is None:
        return None

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return cart_item

def remove_from_cart(request, product_id):
    from products.models import Dish
    if not getattr(request.user, 'is_authenticated', False):
        return
    product = Dish.objects.get(id=product_id)
    cart = get_or_create_cart(request)
    if cart is None:
        return

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        return

def get_cart_items(request):
    cart = get_or_create_cart(request)
    if cart is None:
        return CartItem.objects.none()
    return CartItem.objects.filter(cart=cart).order_by('created_at', 'id')

def get_cart_total(request):
    items = get_cart_items(request)
    return sum(item.total_price for item in items)

def clear_cart(request):
    cart = get_or_create_cart(request)
    if cart is None:
        return
    cart.items.all().delete()