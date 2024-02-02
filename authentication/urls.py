from django.urls import path
from . import views

urlpatterns = [
    path('', views.check_login_or_main, name='send_otp'),
    
]