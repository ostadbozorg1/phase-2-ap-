from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from .models import UserModel,ClinicModel


def do_login(request):
    print("man zendam")
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print("username")
        print("password")
        try:
            user = UserModel.objects.get(username=username, password=password)
        except:
            return redirect('/login?msg=Wrong username or password')
        if user is not None:
            print("lets go")
            request.session['username'] = username
            return redirect('/panel/?msg=Welcome')
        else:
            return redirect('/login?msg=Wrong username or password')
    else:
        print("umm")
        return redirect('/login?msg=Method not allowed')
