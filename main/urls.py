from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main'

urlpatterns = [
    path('', views.show_main, name='show_main'), 
    path('account/', views.account_page, name='account'),
    path('products/', views.products_page, name='products'),
    path('cart/', views.cart_page, name='cart'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)