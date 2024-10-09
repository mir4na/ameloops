from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ProductForm, CategoryForm
from main.models import Product, Category, Cart, CartItem
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import strip_tags

def show_main(request):
    context = {
        'name': 'Muhammad Afwan Hafizh',
        'class': 'PBP F',
        'npm': '2306208855',
        'app_name': 'Ameloops'
    }
    return render(request, "main.html", context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()), max_age=1800)
            messages.success(request, 'Login berhasil!')
            return response
        else:
            messages.error(request, 'Wrong username or password!')
    
    return render(request, 'login.html')

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() 
            Cart.objects.create(user=user)
            messages.success(request, 'Successfully created an account!')
            return redirect('main:login')
        else:
            messages.error(request, 'Wrong input!')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})

@login_required(login_url='/login')
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def products_page(request):
    product_entries = Product.objects.all()
    categories = Category.objects.all()
    context = {
        'product_entries': product_entries,
        'categories': categories
    }
    return render(request, 'products.html', context)

@login_required(login_url='/login')
def get_cart_data(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    total = sum(item.total_price for item in cart_items) if cart_items.exists() else 0
    
    cart_data = []
    for item in cart_items:
        cart_data.append({
            'id': str(item.id),
            'product_name': item.product.name,
            'product_price': item.product.price,
            'quantity': item.quantity,
            'total_price': item.total_price,
            'image_url': item.product.image.url if item.product.image else '',
            'stock': item.product.stock,
        })
    
    return JsonResponse({
        'cart_items': cart_data,
        'total': total,
    })

@login_required(login_url='/login')
def cart_page(request):
    return render(request, 'cart.html')

@require_POST
@login_required(login_url='/login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    return JsonResponse({'status': 'success', 'message': f'{product.name} added to cart'})

@login_required(login_url='/login')
def account_page(request):
    if request.method == 'POST':
        if 'category_name' in request.POST:
            category_name = request.POST['category_name']
            Category.objects.create(name=category_name)
            return redirect('main:products')
        else:
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('main:products') 
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'last_login': request.COOKIES.get('last_login'),
    }
    return render(request, 'account.html', context)

@login_required(login_url='/login')
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.delete()
    return HttpResponseRedirect(reverse('main:cart'))

@login_required(login_url='/login')
def edit_product(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity', 1))
        if new_quantity > 0 and new_quantity <= cart_item.product.stock:
            cart_item.quantity = new_quantity
            cart_item.save()
        else:
            messages.error(request, 'Invalid quantity.')
    return HttpResponseRedirect(reverse('main:cart'))

def create_product_entry(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('main:products')
        else:
            return render(request, "account.html", {'form': form, 'error': 'Form is invalid'})
    return render(request, "account.html", {'form': form})

def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:account')
    else:
        form = CategoryForm()
    return render(request, 'account.html', {'category_form': form})

@csrf_exempt
@require_POST
def create_product_ajax(request):
    if request.method == 'POST':
        cleaned_data = {key: strip_tags(value) for key, value in request.POST.items()}
        form = ProductForm(cleaned_data, request.FILES)
        if form.is_valid():
            product = form.save()
            return JsonResponse({
                "status": "success",
                "message": "Product added successfully",
                "product": serializers.serialize('json', [product])[1:-1]
            }, status=200)
        else:
            return JsonResponse({"status": "error", "message": str(form.errors)}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)

@csrf_exempt
@require_POST
def create_category_ajax(request):
    if request.method == 'POST':
        cleaned_data = {key: strip_tags(value) for key, value in request.POST.items()}
        form = CategoryForm(cleaned_data)
        if form.is_valid():
            category = form.save()
            return JsonResponse({
                "status": "success",
                "message": "Category added successfully",
                "category": serializers.serialize('json', [category])[1:-1]
            }, status=200)
        else:
            return JsonResponse({"status": "error", "message": str(form.errors)}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)

def serialize_data(request, model, fmt, id=None):
    if id:
        data = get_object_or_404(model, pk=id)
        data = [data]
    else:
        data = model.objects.all()
    return HttpResponse(serializers.serialize(fmt, data), content_type=f"application/{fmt}")

def products_json(request):
    return serialize_data(request, Product, "json")

def products_xml(request):
    return serialize_data(request, Product, "xml")

def product_json_by_id(request, id):
    return serialize_data(request, Product, "json", id)

def product_xml_by_id(request, id):
    return serialize_data(request, Product, "xml", id)

def category_json(request):
    return serialize_data(request, Category, "json")

def category_xml(request):
    return serialize_data(request, Category, "xml")

def category_json_by_id(request, id):
    return serialize_data(request, Category, "json", id)

def category_xml_by_id(request, id):
    return serialize_data(request, Category, "xml", id)