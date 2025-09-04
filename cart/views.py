from django.shortcuts import render, redirect
from store.models import Product, Variations
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    # if user is not authenticated
    current_user = request.user
    # If user is not authenticated
    if current_user.is_authenticated:
        product_variations = []
        product = Product.objects.get(id = product_id) # Get the product
        if request.method == "POST":
            for key, value in request.POST.items():
                if key in ['csrfmiddlewaretoken']:
                    continue
            
                try:
                    variation = Variations.objects.get(
                        product = product,
                        variation_category__iexact=key,
                        variation_value__iexact=value
                    )
                    product_variations.append(variation)
                except:
                    pass
        
        is_cart_item_exists = CartItem.objects.filter(product = product, user = current_user).exists()
        if is_cart_item_exists:
            # cart_item = CartItem.objects.get(product = product, cart=cart)
            cart_item = CartItem.objects.filter(product = product, user = current_user)
            existing_variation_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variation.all()
                existing_variation_list.append(list(existing_variation))
                id.append(item.id)
            print(existing_variation_list)
            
            if product_variations in existing_variation_list:
                # increase the item quantity
                index = existing_variation_list.index(product_variations)
                item_id = id[index]
                item = CartItem.objects.get(product = product, id = item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product = product, quantity = 1, user = current_user)
                if len(product_variations) > 0:
                    item.variation.add(*product_variations)
                    # cart_item.quantity += 1
                    item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user
            )
            if len(product_variations) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variations)
            cart_item.save()
            
        return redirect('cart')

    else:
        product_variations = []
        product = Product.objects.get(id = product_id) # Get the product
        if request.method == "POST":
            for key, value in request.POST.items():
                if key in ['csrfmiddlewaretoken']:
                    continue
            
                try:
                    variation = Variations.objects.get(
                        product = product,
                        variation_category__iexact=key,
                        variation_value__iexact=value
                    )
                    product_variations.append(variation)
                    # print(f"Variation - Product - {product} - {variation}")
                except:
                    pass
            
        print(product_variations)
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request)) # Get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()
        
        is_cart_item_exists = CartItem.objects.filter(product = product, cart = cart).exists()
        if is_cart_item_exists:
            # cart_item = CartItem.objects.get(product = product, cart=cart)
            cart_item = CartItem.objects.filter(product = product, cart = cart)
            # existing variation in database
            # current variation -> product_variation
            # item_id -> database
            existing_variation_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variation.all()
                existing_variation_list.append(list(existing_variation))
                id.append(item.id)
            print(existing_variation_list)
            
            if product_variations in existing_variation_list:
                # increase the item quantity
                index = existing_variation_list.index(product_variations)
                item_id = id[index]
                item = CartItem.objects.get(product = product, id = item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product = product, quantity = 1, cart = cart)
                if len(product_variations) > 0:
                    item.variation.add(*product_variations)
                    # cart_item.quantity += 1
                    item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart
            )
            if len(product_variations) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variations)
            cart_item.save()
            
        return redirect('cart')
    
def remove_cart(request, product_id, cart_item_id):
    product = Product.objects.get(id = product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product = product, user = request.user, id = cart_item_id)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_item = CartItem.objects.get(product = product, cart = cart, id = cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    
    product = Product.objects.get(id = product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product = product, user = request.user, id = cart_item_id)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_item = CartItem.objects.get(product = product, cart = cart, id = cart_item_id)
    except:
        pass
    cart_item.delete()
    return redirect('cart')

def cart(request, total = 0, quantity = 0, cart_items = None):
    grand_total = 0
    tax = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user = request.user, is_active = True)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart = cart, is_active = True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            tax = (cart_item.product.tax * total) / 100
        grand_total = total + tax
        
    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'grand_total' : grand_total,
        'tax' : tax
    }
    return render(request, 'cart/cart.html', context)


@login_required(login_url = '')
def checkout(request, total = 0, quantity = 0, cart_items = None):
    grand_total = 0
    tax = 0
    try:
        # cart = Cart.objects.get(cart_id = _cart_id(request))
        # cart_items = CartItem.objects.filter(cart = cart, is_active = True)
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user = request.user, is_active = True)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart = cart, is_active = True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            tax = (cart_item.product.tax * total) / 100 
        grand_total = total + tax
        
        
    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'grand_total' : grand_total,
        'tax' : tax
    }
    return render(request, 'cart/checkout.html', context)