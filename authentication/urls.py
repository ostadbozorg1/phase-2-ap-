from django.urls import path
from . import views

urlpatterns = [
    path('', views.check_login_or_main, name='send_otp'),
    path('login/', views.login_page, name='send_otp'),
    path('do_login/', views.do_login, name='send_otp'),
    path('do_signup/', views.do_signup, name='send_otp'),
    path('do_add_clinic/', views.do_add_clinic, name='send_otp'),

    
]