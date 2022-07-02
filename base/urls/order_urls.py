from django.urls import path
from ..views import order_views as views

urlpatterns = [
    path('', views.getOrders, name='orders'),
    path('add/', views.addOrderItems, name='order_add'),
    path('myorders/', views.getMyOrders, name='my_orders'),
    path('<str:pk>/deliver/', views.updateOrderToDelivered, name='deliver'),
    path('<str:pk>/', views.getOrderById, name='order_detail'),
]