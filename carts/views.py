from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, CartItem
from store.models import Product, Variation
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

def _cart_id(request):
    cart_id = request.session.get('cart_id')
    if not cart_id:
        if not request.session.session_key:
            request.session.create()
        cart_id = request.session.session_key
        request.session['cart_id'] = cart_id
    return cart_id
from django.shortcuts import get_object_or_404, redirect
from django.db.models import QuerySet

def add_cart(request, product_id):
    current_user = request.user
    product = get_object_or_404(Product, id=product_id)

    # Function to get variations from POST data
    def get_variations():
        variations = []
        if request.method == 'POST':
            for key in request.POST:
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(
                        product=product,
                        variation_category__iexact=key,
                        variation_value__iexact=value
                    )
                    variations.append(variation)
                except Variation.DoesNotExist:
                    pass
        return variations

    if current_user.is_authenticated:
        product_variations = get_variations()
        
        # Check if cart item exists for authenticated user
        cart_items = CartItem.objects.filter(product=product, user=current_user)
        if cart_items.exists():
            ex_var_list = []
            id_list = []
            for item in cart_items:
                existing_variations = list(item.variations.all())
                ex_var_list.append(existing_variations)
                id_list.append(item.id)

            if product_variations in ex_var_list:
                index = ex_var_list.index(product_variations)
                item_id = id_list[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if product_variations:
                    item.variations.add(*product_variations)
                item.save()
        else:
            cart_item = CartItem.objects.create(product=product, quantity=1, user=current_user)
            if product_variations:
                cart_item.variations.add(*product_variations)
            cart_item.save()

    else:  # Unauthenticated user
        product_variations = get_variations()
        
        # Get or create cart
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
            cart.save()

        cart_items = CartItem.objects.filter(product=product, cart=cart)
        if cart_items.exists():
            ex_var_list = []
            id_list = []
            for item in cart_items:
                existing_variations = list(item.variations.all())
                ex_var_list.append(existing_variations)
                id_list.append(item.id)

            if product_variations in ex_var_list:
                index = ex_var_list.index(product_variations)
                item_id = id_list[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if product_variations:
                    item.variations.add(*product_variations)
                item.save()
        else:
            cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if product_variations:
                cart_item.variations.add(*product_variations)
            cart_item.save()

    return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(
                product=product, 
                user=request.user, 
                id=cart_item_id
            )
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(
                product=product, 
                cart=cart, 
                id=cart_item_id
            )
            
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except (CartItem.DoesNotExist, Cart.DoesNotExist):
        pass
    
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(
                product=product, 
                user=request.user, 
                id=cart_item_id
            )
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(
                product=product, 
                cart=cart, 
                id=cart_item_id
            )
        cart_item.delete()
    except (CartItem.DoesNotExist, Cart.DoesNotExist):
        pass
    
    return redirect('cart')

def cart(request):
    total = 0
    quantity = 0
    cart_items = None
    tax = 0
    grand_total = 0

    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        
        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)

@login_required(login_url='login')
def checkout(request):
    total = 0
    quantity = 0
    cart_items = None
    tax = 0
    grand_total = 0

    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context)

def place_order(request):
    return render(request, 'store/place_order.html')