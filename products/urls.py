from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path('', views.menuPage, name='menuPage'),
    path('<slug:slug>/', views.category_detail, name='category'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product'),
]