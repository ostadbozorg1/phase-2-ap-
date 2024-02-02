from django.urls import path
from . import views

urlpatterns = [
    path('', views.panel, name='send_otp'),
    path('new_appointment/', views.new_appointment, name='send_otp'),
    path('make_new_appointment/', views.make_new_appointment, name='send_otp'),
]