from django.urls import path
from . import views

urlpatterns = [
    path('', views.panel, name='send_otp'),
    path('new_appointment/', views.new_appointment, name='send_otp'),
    path('make_new_appointment/', views.make_new_appointment, name='send_otp'),
    path('my_appointments/', views.my_appointments, name='send_otp'),
    path('cancel_appointment/', views.cancel_appointment, name='send_otp'),
    path('list_clinics/', views.list_clinics, name='send_otp'),
    path('logout/', views.make_logout, name='send_otp'),
]