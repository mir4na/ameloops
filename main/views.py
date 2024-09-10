from django.shortcuts import render

def show_main(request):
    context = {
        'npm' : '2306208855',
        'name': 'Muhammad Afwan Hafizh',
        'class': 'PBP F'
    }

    return render(request, "main.html", context)
