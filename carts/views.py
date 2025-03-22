from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, CartItem
from store.models import Product, Variation
from django.core.exceptions import ObjectDoesNotExist


def _cart_id(request):
    # Generate a unique cart ID for the session
    cart_id = request.session.get('cart_id')
    if not cart_id:
        cart_id = request.session.session_key
        request.session['cart_id'] = cart_id
    return cart_id



# def add_cart(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     product_variation = []
#     if request.method == 'POST':
#         for item in request.POST:
#             key = item
#             value = request.POST[key]

#             try:
#                 variations = Variation.objects.filter(
#                     product=product,
#                     variation_category__iexact=key,
#                     variation_value__iexact=value
#                 )
#                 if variations.exists():
#                     product_variation.append(variations.first())  # Use the first matching variation
#             except Variation.DoesNotExist:
#                 pass

#     # Get or create the cart
#     cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))

#     # Check if the cart item with the same product and variations already exists
#     cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
#     if cart_item_exists:
#         cart_items = CartItem.objects.filter(product=product, cart=cart)
#         for item in cart_items:
#             existing_variations = list(item.variations.all())
#             if existing_variations == product_variation:
#                 # If the same product with the same variations exists, increase the quantity
#                 item.quantity += 1
#                 item.save()
#                 break
#         else:
#             # If no matching item is found, create a new cart item
#             cart_item = CartItem.objects.create(
#                 product=product,
#                 quantity=1,
#                 cart=cart,
#             )
#             if product_variation:
#                 cart_item.variations.add(*product_variation)
#     else:
#         # If no cart item exists for this product, create a new one
#         cart_item = CartItem.objects.create(
#             product=product,
#             quantity=1,
#             cart=cart,
#         )
#         if product_variation:
#             cart_item.variations.add(*product_variation)

#     return redirect('cart')




def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value
                )
                product_variation.append(variation)
            except Variation.DoesNotExist:
                pass

    # Get or create the cart
    cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))

    # Check if the cart item with the same product and variations already exists
    cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
    if cart_item_exists:
        cart_items = CartItem.objects.filter(product=product, cart=cart)
        for item in cart_items:
            existing_variations = list(item.variations.all())
            if existing_variations == product_variation:
                # If the same product with the same variations exists, increase the quantity
                item.quantity += 1
                item.save()
                break
        else:
            # If no matching item is found, create a new cart item
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
            if product_variation:
                cart_item.variations.add(*product_variation)
    else:
        # If no cart item exists for this product, create a new one
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        if product_variation:
            cart_item.variations.add(*product_variation)

    return redirect('cart')


def remove_cart(request, product_id,cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)

    try:

        cart_item = CartItem.objects.get(product=product, cart=cart,id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id,cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart,id=cart_item_id)
    cart_item.delete()

    return redirect('cart')


def cart(request):
    total = 0
    quantity = 0
    cart_items = None
    tax = 0
    grand_total = 0

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total) / 100  # Example tax calculation (2%)
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass  # Handle the case where the cart does not exist

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)


def checkout(request):
    return render(request, 'store/checkout.html')