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
    path('pending_appointments/', views.pending_appointments, name='send_otp'),
    path('approve_appointment/', views.approve_appointment, name='send_otp'),
    path('confirmed_appointments/', views.confirmed_appointments, name='send_otp'),
    path('canceled_appointments/', views.canceled_appointments, name='send_otp'),
    path('passed_appointments/', views.passed_appointments, name='send_otp'),

]