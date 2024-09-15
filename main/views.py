from django.shortcuts import render, redirect
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
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('main:products')
    context = {'form': form}
    return render(request, "account.html", context)

def products_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def products_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def product_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def product_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
