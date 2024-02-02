from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout
from authentication.models import UserModel, ClinicModel, Appointment
from datetime import datetime
from datetime import date

