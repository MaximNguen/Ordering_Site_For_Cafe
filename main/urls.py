from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.home, name='index'),
    path('vacancies/', views.vacancies, name='vacancies'),
    path('promotions/', views.promotions, name='promo'),
]