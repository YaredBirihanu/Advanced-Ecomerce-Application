from django.shortcuts import render,get_object_or_404
from django.contrib import messages
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q
from .models import Product,ReviewRating
from carts.models import CartItem
from category.models import Category
from carts.views import _cart_id
from orders.models import Order,OrderProduct


# def submit_review(request,product_id):
#     url=request.META.get('HTTP_REFFERER')
#     if request.method == 'POST':
#         try:
#             reviews=ReviewRating.objects.get(user__id=request.user.id,product__id=product.id)
#             form=ReviewRatingform(request.POST,instance=reviews)
#             form.save()
#             messages.success(request,'Thanks for your review')
#             return redirect(url)
#         except ReviewRating.DoesNotExist:
#             form=ReviewRatingform(request.POST,instance=reviews)
#             if form.is_valid():
#                 data=ReviewRating()
#                 data.subject=form.cleaned_data['subject']
#                 data.rating=form.cleaned_data['rating']
#                 data.review=form.cleaned_data['review']
#                 data.ip=form.cleaned_data['ip']
#                 data.product_id=product_id
#                 data.user_id=request.user.id
#                 data.save()
#                 messages.success(request,'Thank you your review is sumbited')
#                 return redirect(url)



def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 2)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count=products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()


    # # Pagination
    # paginator = Paginator(products, 6)
    # page = request.GET.get('page')
    # try:
    #     paged_products = paginator.get_page(page)
    # except PageNotAnInteger:
    #     paged_products = paginator.get_page(1)
    # except EmptyPage:
    #     paged_products = paginator.get_page(paginator.num_pages)

    # product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
        #'categories': categories,  # Optional: Add category information
    }
    return render(request, 'store/store.html', context)



def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
    
    

    # {% if request.user.is_authenticated %}
    # try:
    #     orderproduct=OrderProduct.objects.filter(user=request.user,product_id=single_product.id).exists()
    # except OrderProduct.DoesNotExist:
    #     orderproduct=None
    # {% else %}
    #     orderproduct=None


    # reviews=ReviewRating.objects.filter(product_id=single_product.id,status=True)    

    context = {
        'single_product': single_product,
        'in_cart': in_cart,  # Optional: Add cart functionality if needed
        #'orderproduct':orderproduct,
    }
    return render(request, 'store/product_detail.html', context)

def search(request):
    product_count=0
    products = Product.objects.order_by('-created_date')
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = products.filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)