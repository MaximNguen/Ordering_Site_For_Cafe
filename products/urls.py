from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path('', views.menuPage, name='menuPage'),
    path('<slug:slug>/', views.category_detail, name='category')
]