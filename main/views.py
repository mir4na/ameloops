from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ProductForm
from main.models import Product, Category
from django.http import HttpResponse
from django.core import serializers

def show_main(request):
    context = {
        'npm': '2306208855',
        'name': 'Muhammad Afwan Hafizh',
        'class': 'PBP F',
        'app_name': 'Ameloops',
    }
    return render(request, "main.html", context)

def products_page(request):
    product_entries = Product.objects.all()
    categories = Category.objects.all()
    context = {
        'product_entries': product_entries,
        'categories': categories
    }
    return render(request, 'products.html', context)

def cart_page(request):
    return render(request, 'cart.html')

def create_product_entry(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('main:products')
        else:
            return render(request, "account.html", {'form': form, 'error': 'Form is invalid'})
    return render(request, "account.html", {'form': form})

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