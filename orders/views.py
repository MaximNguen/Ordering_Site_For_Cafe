from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.utils import get_cart_items, get_cart_total
from .forms import OrderForm
from .models import Order, OrderItem
from cart.models import CartItem, Cart

@login_required
def create_order(request):
    cart_items = get_cart_items(request)
    total = get_cart_total(request)

    if not cart_items.exists():
        return render(request, 'cart/cart_detail.html', {'cart_items': cart_items})

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            current_cart = request.user.cart_set.first()

            if hasattr(current_cart, 'order'):
                return redirect('orders:order_detail', order_id=current_cart.order.id)
            
            order = form.save(commit=False)
            order.user = request.user
            order.cart = current_cart
            order.total_price = total
            order.save()

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product = item.product,
                    quantity = item.quantity,
                    price = item.product.price,
                )

            # Clear the cart items after order is created
            current_cart.items.all().delete()
            return redirect('orders:order_detail', order_id=order.id)

    else:
        form = OrderForm()

    return render(request, 'orders/create_order.html', {
        'form': form,
        'cart_items': cart_items,
        'total': total,
    })


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})