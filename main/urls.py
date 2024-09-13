from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.show_main, name='show_main'), 
    path('account/', views.account_page, name='account'),
    path('products/', views.products_page, name='products'),
    path('cart/', views.cart_page, name='cart'),
]