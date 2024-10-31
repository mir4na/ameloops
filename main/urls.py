from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.show_main, name='show_main'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('products/', views.products_page, name='products'),

    path('cart/', views.cart_page, name='cart'),
    path('get-cart-data/', views.get_cart_data, name='get_cart_data'),
    
    path('add-to-cart/<uuid:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<uuid:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('edit-cart-item/<uuid:cart_item_id>/', views.edit_product, name='edit_cart_item'),

    path('create-product-ajax/', views.create_product_ajax, name='create_product_ajax'),
    path('create-category-ajax/', views.create_category_ajax, name='create_category_ajax'),

    path('account/product-entry/', views.create_product_entry, name='create_product_entry') ,
    path('create-category/', views.create_category, name='create_category'),
    path('account/', views.account_page, name='account'),

    path('product_json/', views.products_json, name='products_json'),
    path('product_xml/', views.products_xml, name='products_xml'),
    path('product_json/<str:id>/', views.product_json_by_id, name='product_json_by_id'),
    path('product_xml/<str:id>/', views.product_xml_by_id, name='product_xml_by_id'),
    path('category_json/', views.category_json, name='category_json'),
    path('category_xml/', views.category_xml, name='category_xml'),
    path('category_json/<str:id>/', views.category_json_by_id, name='category_json_by_id'),
    path('category_xml/<str:id>/', views.category_xml_by_id, name='category_xml_by_id'),
]