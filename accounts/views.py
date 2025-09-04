from django.shortcuts import render, redirect

from cart.models import Cart, CartItem
from cart.views import _cart_id
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Account

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            username = email.split("@")[0]
            password = form.cleaned_data["password"]
            if Account.objects.filter(email=email).exists():
                form.add_error("email", "Account already exists")
            else:
                user = Account.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=password,
                )
            user.save()
            # messages.success(request, "Registration successfull.")
            
            return redirect("login")
        else:
            pass
    else:
        form = RegistrationForm()
    context = {"form": form}
    return render(request, "accounts/register.html", context)
def login_page(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email = email, password = password)
            if user is not None:
                try:
                    cart = Cart.objects.get(cart_id = _cart_id(request))
                    is_cart_item_exists = CartItem.objects.filter(cart= cart).exists()
                    if is_cart_item_exists:
                        cart_item = CartItem.objects.filter(cart = cart)
                        
                        # Getting product variations by cart id
                        product_variation = []
                        for item in cart_item:
                            variation = item.variation.all()
                            product_variation.append(list(variation))
                            
                        # Get the cart items from the user to access his product variations
                        cart_item = CartItem.objects.filter(user = user)
                        existing_variation_list = []
                        id = []
                        for item in cart_item:
                            existing_variation = item.variation.all()
                            existing_variation_list.append(list(existing_variation))
                            id.append(item.id)
                            
                        for pr in product_variation:
                            if pr in existing_variation_list:
                                index = existing_variation_list.index(pr)
                                item_id = id[index]
                                item = CartItem.objects.get(id = item_id)
                                item.quantity += 1
                                item.user = user
                                item.save()
                                
                            else:
                                cart_item = CartItem.objects.filter(cart = cart)
                                for item in cart_item:
                                    item.user = user
                                    item.save()
                        
                        
                except:
                    pass
                login(request, user)
                return redirect('store')
            else:
                messages.error(request, 'Invalid email or password!')
    else:
        form = LoginForm()
    context = {'form' : form}
    return render(request, 'accounts/login.html', context)

def logout_page(request):
    logout(request)
    return redirect('home')


def dashboard(request):
    return render(request, 'accounts/dashboard.html')