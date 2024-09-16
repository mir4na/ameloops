from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.show_main, name='show_main'),
    path('products/', views.products_page, name='products'),
    path('cart/', views.cart_page, name='cart'),
    path('account/', views.create_product_entry, name='create_product_entry'),
    path('product_json/', views.products_json, name='products_json'),
    path('product_xml/', views.products_xml, name='products_xml'),
    path('product_json/<str:id>/', views.product_json_by_id, name='product_json_by_id'),
    path('product_xml/<str:id>/', views.product_xml_by_id, name='product_xml_by_id'),
    path('category_json/', views.category_json, name='category_json'),
    path('category_xml/', views.category_xml, name='category_xml'),
    path('category_json/<str:id>/', views.category_json_by_id, name='category_json_by_id'),
    path('category_xml/<str:id>/', views.category_xml_by_id, name='category_xml_by_id')
]
