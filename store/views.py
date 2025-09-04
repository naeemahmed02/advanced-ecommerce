from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from cart.models import CartItem
from cart.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.db.models import Q



def store(request, category_slug = None):
    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug= category_slug)
        products = Product.objects.filter(category = categories, is_available = True).order_by('-created_date')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    else:
        products = Product.objects.all().filter(is_available = True).order_by('-created_date')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    context = {'products' : paged_products}
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = get_object_or_404(Product, category__slug = category_slug, slug = product_slug)
        print(single_product)
        in_cart = CartItem.objects.filter(cart__cart_id= _cart_id(request), product = single_product).exists()
    except Exception as e:
        raise e
    colors = single_product.variations_set.filter(variation_category='color', is_active=True)
    sizes = single_product.variations_set.filter(variation_category='size', is_active=True)
    context = {'single_product': single_product, 'in_cart' : in_cart, 'colors': colors, 'sizes': sizes}
    return render(request, 'store/product_detail.html', context)

def search(request):
    searched_products = None
    if 'keyword' in request.GET:
        keyword = request.GET.get('keyword')
        if keyword:
            searched_products = Product.objects.filter(Q(name__icontains = keyword) | Q(product_description__icontains = keyword))
    context = {'products' : searched_products}
    return render(request, 'store/store.html', context)
 