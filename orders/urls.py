from django.urls import path
from . import views, api

app_name = 'orders'

urlpatterns = [
    path('create/', views.create_order, name='create_order'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('', views.order_list, name='order_list'),
    path('api/bot/<int:order_id>/<str:action>/', api.bot_update_status, name='bot_update_status'),
    path('payment/<int:order_id>/', views.payment_callback, name='payment_callback'),
]