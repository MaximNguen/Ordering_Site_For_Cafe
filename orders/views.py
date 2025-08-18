import uuid

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.utils import get_cart_items, get_cart_total
from .forms import OrderForm
from .integrations import send_order_to_bot
from .models import Order, OrderItem
from yookassa import Configuration, Payment

Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

@login_required
def create_order(request):
    cart_items = get_cart_items(request)
    total = get_cart_total(request)

    if not cart_items.exists():
        return render(request, 'cart/cart_detail.html', {'cart_items': cart_items})

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            payment_method = form.cleaned_data.get('payment_method')
            delivery_method = form.cleaned_data.get('delivery_method')
            if delivery_method == 'delivery' and total < 1500:
                form.add_error('delivery_method', 'Минимальная сумма заказа для доставки - 1500 рублей')
                return render(request, 'orders/create_order.html', {
                    'form': form,
                    'cart_items': cart_items,
                    'total': total,
                    'delivery_price': 150,
                })

            if delivery_method == 'delivery' and total >= 1500:
                total = total + 150

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

            if payment_method == "card":
                payment = Payment().create({
                    "amount": {
                        "value": str(total),
                        "currency": "RUB"
                    },
                    "confirmation": {
                        "type": "redirect",
                        "return_url": settings.YOOKASSA_RETURN_URL + str(order.id) + '/'
                    },
                    "capture": True,
                    "description": f"Оплата заказа #{order.id}",
                    "metadata": {
                        "order_id": order.id
                    }}, str(uuid.uuid4())
                )

                order.payment_id = payment.id
                order.save()

                return redirect(payment.confirmation.confirmation_url)
            else:
                current_cart.items.all().delete()
                try:
                    print(">>> Создаём заказ и отправляем в бота")
                    send_order_to_bot(order)
                except Exception as e:
                    pass

                return redirect('orders:order_detail', order_id=order.id)

    else:
        form = OrderForm()

    return render(request, 'orders/create_order.html', {
            'form': form,
            'cart_items': cart_items,
            'total': total,
            'delivery_price': 150,
        })


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def payment_callback(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.payment_id:
        payment = Payment.find_one(order.payment_id)
        if payment.status == 'succeeded':
            order.is_paid = True
            order.status = 'paid'
            order.save()
            request.user.cart_set.first().items.all().delete()
            try:
                send_order_to_bot(order)
            except Exception as e:
                pass
            return redirect('orders:order_detail', order_id=order.id)

    return redirect('orders:order_detail', order_id=order.id)