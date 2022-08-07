from django.urls import path
from django.views.generic import TemplateView
from .views import *


urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('payment-guideline/', PaymentGuideline.as_view(), name="payment-guideline"),
    path('about/', AboutUs.as_view(), name="about"),
    path('contact/', contact_page, name="contact")
]