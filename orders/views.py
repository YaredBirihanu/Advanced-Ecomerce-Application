from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from carts.models import Cart,CartItem
from .forms import OrderForm
from .models import Payment
from .models import Order,OrderProduct
from store.models import Product
import datetime

def order_complete(request):
    order_number=request.GET.get('order_number')
    transID=request.GET.get('trans_id')
    try:
        order=Order.objects.get(order_number=order_number,is_ordered=True)
        ordered_products=OrderProduct.objects.filter(order_id=order.id)
        subtotal=0
        for i in ordered_products:
            subtotal+=i.product_price*i.quantity

        payment=Payment.objects.get(payment_id=payment.id)
        context={
            'order':order,
            'ordered_products':ordered_products,
            'payment':payment,
            'payment_method':payment.payment_method,
            'order_number':order_number,
            'transID':transID,
            'sub_total':subtotal,
            'order_date':datetime.datetime.now()
        }
    return render(request,'orders/order_complete.html',{})


def payments(request):

    #move the cart item to the order product table

    # cart_items=CartItem.object.filter(user=request.user)
    # for item in cart_items:
    #     orderproduct=OrderProduct()
    #     orderproduct.order_id=order.id
    #     orderproduct.payment=payment
    #     orderproduct.user_id=user.id
    #     orderproduct.product_id=item.product.id
    #     orderproduct.quantity=item.quantity
    #     orderproduct.product_price=item.product_price
    #     orderproduct.ordered=True
    #     orderproduct.save()

    # cart_item=CartItem.objects.get(id=item.id)
    # product_variation=cart_item.variations.all()
    # orderproduct=orderproduct.objects.get(id=orderproduct.id)
    # orderproduct.variations,set(product_variation)
    # orderproduct.save()


    # #reduce sold item
    # product=Product.objects.get(id=item.product_id)
    # product.stock -= item.quantity
    # product.save()

    # #clear cart
    # CartItem.objects.get(user=request.user).delete()

    # mail_subject = 'Thank you for your order'
    # message = render_to_string('accounts/order_recieved_email.html', {
    #     'user': request.user,
    #     'order':order,
            
    #     })
    #     to_email = request.user.email
    #     send_email = EmailMessage(mail_subject, message, to=[to_email])
    #     send_email.send()

    data={
        'order_number':order_number,
        'transID':payment.product_id,
    }
    
    return render(request,'orders/payments.html')

    




    


def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total) / 100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get['REMOTE_ADDR']
            data.user = current_user
            data.save()

            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime('%Y%m%d')
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order=Order.objects.get(user=current_user,is_ordered=False,order_number=order_number) 
            context = {
                'order':order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payments.html', context)
        
    else:
        return redirect('checkout')
    

    # else:
    #     form = OrderForm()
    #     context = {
    #         'order':order,
    #         'cart_items': cart_items,
    #         'total': total,
    #         'tax': tax,
    #         'grand_total': grand_total,
    #     }
    #     return render(request, 'store/checkout.html', context)