import razorpay
import math
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from carts.models import CartItem

from .models import Order, Payment
from .forms import OrderForm
from datetime import date
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.urls import reverse
from django.core.mail import send_mail

def get_razorpay_client():
    """Get Razorpay client with validation"""
    key_id = settings.RAZORPAY_KEY_ID
    key_secret = settings.RAZORPAY_KEY_SECRET
    
    if not key_id or not key_secret:
        raise ValueError("Razorpay keys are not configured. Please set RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET in your .env file.")
    
    return razorpay.Client(auth=(key_id, key_secret))


@login_required
def place_order(request):
    if request.method == "POST":
        # Try to find an existing pending order; otherwise create one from the checkout form
        order = Order.objects.filter(user=request.user, is_ordered=False).last()
        if not order:
            cart_items_qs = CartItem.objects.filter(user=request.user, is_active=True)
            if not cart_items_qs.exists():
                return redirect('cart')

            # Compute totals similar to checkout
            total_amount = 0
            for item in cart_items_qs:
                total_amount += float(item.product.price) * int(item.quantity)
            tax_amount = (2 * total_amount) / 100

            # Build order from POST
            order = Order(
                user=request.user,
                first_name=request.POST.get('first_name', ''),
                last_name=request.POST.get('last_name', ''),
                phone=request.POST.get('phone', ''),
                email=request.POST.get('email', ''),
                address_line_1=request.POST.get('address_line_1', ''),
                address_line_2=request.POST.get('address_line_2', ''),
                country=request.POST.get('country', ''),
                state=request.POST.get('state', ''),
                city=request.POST.get('city', ''),
                order_note=request.POST.get('order_note', ''),
                order_total=total_amount,
                tax=tax_amount,
                ip=request.META.get('REMOTE_ADDR', ''),
                is_ordered=False,
            )
            order.save()
            # Generate and save order number
            today_str = date.today().strftime('%Y%m%d')
            order.order_number = f"{today_str}{order.id}"
            order.save()

        # Collect cart items for display and compute payable amount (order_total + tax)
        cart_items = CartItem.objects.filter(user=request.user)
        payable_total = (order.order_total or 0) + (order.tax or 0)
        # Amount in paise; round up and enforce minimum ₹1.00 (100 paise)
        amount = max(100, int(math.ceil(payable_total * 100)))

        # Create Razorpay order
        try:
            client = get_razorpay_client()
            razorpay_order = client.order.create({
                "amount": amount,
                "currency": "INR",
                "payment_capture": 1
            })
        except ValueError as e:
            # Configuration error - keys not set
            error_msg = "Payment gateway configuration error. Please ensure RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET are set in your .env file."
            return render(request, 'orders/payment_error.html', {'error': error_msg})
        except razorpay.errors.BadRequestError as e:
            # Razorpay API error
            error_msg = f"Payment gateway error: {str(e)}"
            return render(request, 'orders/payment_error.html', {'error': error_msg})
        except Exception as e:
            # Any other error
            error_msg = f"An error occurred while processing your payment: {str(e)}"
            return render(request, 'orders/payment_error.html', {'error': error_msg})

        # Persist the created Razorpay order id on our Order for later verification
        order.razorpay_order_id = razorpay_order['id']
        order.save()

        # Pass the order info to template
        context = {
            'order': order,
            'cart_items': cart_items,
            'total': order.order_total,
            'tax': order.tax,
            'grand_total': payable_total,
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
            'amount': amount,
            'currency': 'INR',
        }
        return render(request, 'orders/payments.html', context)

    # If GET request, redirect to checkout/cart
    return redirect('cart')


def payments(request):
    current_user = request.user

    # Get the first pending order (if multiple exist)
    order = Order.objects.filter(user=current_user, is_ordered=False).first()
    if not order:
        return redirect('store')

    # Razorpay order creation
    try:
        client = get_razorpay_client()
        payable_total = (order.order_total or 0) + (order.tax or 0)
        # Round up and enforce minimum ₹1.00 (100 paise)
        amount = max(100, int(math.ceil(payable_total * 100)))
        razorpay_order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1
        })
    except Exception as e:
        return render(request, 'orders/payment_error.html', {'error': str(e)})

    order.razorpay_order_id = razorpay_order['id']
    order.save()

    cart_items = CartItem.objects.filter(user=current_user)
    context = {
        'order': order,
        'cart_items': cart_items,
        'total': order.order_total,
        'tax': order.tax,
        'grand_total': payable_total,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
        'amount': amount,
        'currency': 'INR',
    }
    return render(request, 'orders/payments.html', context)



@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')

        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        try:
            client = get_razorpay_client()
            client.utility.verify_payment_signature(params_dict)

            order = Order.objects.get(razorpay_order_id=order_id)

            with transaction.atomic():
                payment = Payment.objects.create(
                    user=order.user,
                    payment_id=payment_id,
                    payment_method="Razorpay",
                    amount_paid=str(order.order_total),
                    status="Paid"
                )

                # Move cart items to OrderProduct and reduce stock
                cart_items = CartItem.objects.filter(user=order.user)
                from .models import OrderProduct
                for item in cart_items:
                    order_product = OrderProduct.objects.create(
                        order=order,
                        payment=payment,
                        user=order.user,
                        product=item.product,
                        quantity=item.quantity,
                        product_price=float(item.product.price),
                        ordered=True,
                    )
                    if item.variations.exists():
                        order_product.variations.set(item.variations.all())
                    # Reduce product stock
                    item.product.stock = max(0, int(item.product.stock) - int(item.quantity))
                    item.product.save()

                # Clear cart
                cart_items.delete()

                # Mark order completed
                order.payment = payment
                order.is_ordered = True
                order.status = "Completed"
                order.save()

            # Send order email (best-effort)
            try:
                send_mail(
                    subject=f"Order Received — {order.order_number}",
                    message=f"Thank you for your order {order.order_number}. Payment {payment.payment_id} successful.",
                    from_email=None,
                    recipient_list=[order.email],
                    fail_silently=True,
                )
            except Exception:
                pass

            redirect_url = f"{reverse('order_complete')}?order_number={order.order_number}&payment_id={payment.payment_id}"
            return JsonResponse({'status': 'Payment Verified', 'redirect_url': redirect_url})
        except Exception as e:
            return JsonResponse({'status': 'Payment Verification Failed', 'error': str(e)})

def order_complete(request):
    order_number = request.GET.get('order_number')
    payment_id = request.GET.get('payment_id')
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        payment = Payment.objects.get(payment_id=payment_id, user=order.user)
    except (Order.DoesNotExist, Payment.DoesNotExist):
        return HttpResponse("Order not found or not completed.")

    from .models import OrderProduct
    ordered_products = OrderProduct.objects.filter(order=order, ordered=True)
    context = {
        'order': order,
        'payment': payment,
        'ordered_products': ordered_products,
    }
    return render(request, 'orders/order_complete.html', context)