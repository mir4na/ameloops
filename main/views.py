from django.shortcuts import render

def show_main(request):
    context = {
        'npm' : '2306208855',
        'name': 'Muhammad Afwan Hafizh',
        'class': 'PBP F',
        'app_name': 'Amesoup',
    }

    return render(request, "main.html", context)

def account_page(request):
    context = {
        'npm' : '2306208855',
        'name': 'Muhammad Afwan Hafizh',
        'class': 'PBP F',
        'app_name': 'Amesoup',
    }
    return render(request, 'account.html', context)

def products_page(request):
    return render(request, 'products.html')

def cart_page(request):
    return render(request, 'cart.html')