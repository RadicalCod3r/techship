from django.urls import path
from ..views import payment_views as views

urlpatterns = [
    path('test-payment/', views.testPayment, name='test_payment'),
    path('save-stripe-info/', views.saveStripeInfo, name='save_stripe_info'),
]