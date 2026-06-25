from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from store.models import Product
from .models import Cart, CartItem, Order, OrderItem


def get_cart(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user).first()
    sk = request.session.session_key
    return Cart.objects.filter(session_key=sk).first() if sk else None


@login_required
def checkout(request):
    cart = get_cart(request)
    if not cart or cart.item_count == 0:
        messages.warning(request, 'Your cart is empty.')
        return redirect('store:cart')

    shipping_cost = 0 if cart.total >= 500 else 50

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        pincode = request.POST.get('pincode', '').strip()
        payment_method = request.POST.get('payment_method', 'cod')
        notes = request.POST.get('notes', '')

        if not all([full_name, email, phone, address, city, state, pincode]):
            messages.error(request, 'Please fill in all required fields.')
        else:
            with transaction.atomic():
                total = cart.total + shipping_cost
                order = Order.objects.create(
                    user=request.user,
                    full_name=full_name,
                    email=email,
                    phone=phone,
                    address=address,
                    city=city,
                    state=state,
                    pincode=pincode,
                    payment_method=payment_method,
                    subtotal=cart.total,
                    shipping_cost=shipping_cost,
                    total=total,
                    notes=notes,
                )
                for item in cart.items.all():
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.get_price,
                    )
                    # Reduce stock
                    item.product.stock = max(0, item.product.stock - item.quantity)
                    item.product.save()

                cart.items.all().delete()

            messages.success(request, f'Order #{order.order_number} placed successfully!')
            return redirect('orders:order_detail', pk=order.pk)

    return render(request, 'orders/checkout.html', {
        'cart': cart,
        'shipping_cost': shipping_cost,
        'user': request.user,
    })


@login_required
def order_list(request):
    orders = request.user.orders.all()
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def cancel_order(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if order.status in ['pending', 'confirmed']:
        order.status = 'cancelled'
        order.save()
        messages.success(request, 'Order cancelled successfully.')
    else:
        messages.error(request, 'This order cannot be cancelled.')
    return redirect('orders:order_detail', pk=pk)
