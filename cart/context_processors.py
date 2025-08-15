from .utils import get_cart_items, get_cart_total

def cart(request):
    return {
        'cart': get_cart_items(request),
        'cart_total': get_cart_total(request),
    }