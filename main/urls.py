from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.show_main, name='show_main'),
    path('products/', views.products_page, name='products'),
    path('cart/', views.cart_page, name='cart'),
    path('account/', views.create_product_entry, name='create_product_entry'),  # Menambahkan routing untuk create product
    path('json/', views.products_json, name='products_json'),
    path('xml/', views.products_xml, name='products_xml'),
    path('json/<str:id>/', views.product_json_by_id, name='product_json_by_id'),
    path('xml/<str:id>/', views.product_xml_by_id, name='product_xml_by_id'),
]
