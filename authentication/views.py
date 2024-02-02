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


def do_signup(request):
    print("man zendam")
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        name = request.POST['name']
        role = request.POST['role']
        clinic_id = request.POST['clinic_id']
        if(role != "monshi" and role != "patient"):
            return redirect('/login?msg=what is that role you entered bro')
        try:
            user = UserModel.objects.get(username=username)
            return redirect('/login?msg=duplicate username')
        except:
            pass
        try:
            user = UserModel.objects.get(email=email)
            return redirect('/login?msg=duplicate email')
        except:
            pass
        if(role == "monshi"):
            if(len(clinic_id) < 1):
                return redirect('/login?msg=wrong clinic id')
            try:
                user = UserModel.objects.get(clinic_id=clinic_id)
                return redirect('/login?msg=wrong clinic id')
            except:
                pass
        if(len(clinic_id) < 1):
            clinic_id = "not_monshi"
        user = UserModel(username=username, password=password,clinic_id=clinic_id,email=email,name=name,role=role)
        user.save()
        request.session['username'] = username
        return redirect('/panel/?msg=Welcome')
    else:
        print("ummmm")
        return redirect('/login?msg=Method not allowed')

def do_add_clinic(request):
    print("man zendam")
    if request.method == 'POST':
        clinic_id = request.POST['clinic_id']
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        phone_number = request.POST['phone_number']
        services = request.POST['services']
        try:
            user = ClinicModel.objects.get(email=email)
            return redirect('/login?msg=dup email')
        except:
            pass
        try:
            user = ClinicModel.objects.get(clinic_id=clinic_id)
            return redirect('/login?msg=dup clinic id')
        except:
            pass
        clinic = ClinicModel(clinic_id=clinic_id, email=email,name=name,address=address,phone_number=phone_number, services=services)
        clinic.save()
        return redirect('/panel/')
    else:
        print("ummmm")
        return redirect('/login?msg=method not allowed')

def check_login_or_main(request):
    if 'username' in request.session:
        return redirect('/panel/')
    else:
        return redirect('/login/?msg=Please login')

def login_page(request):
    msg = request.GET.get('msg', "nope")
    msg2 = msg.replace(" ","")
    if(msg2.isalpha() is not True):
        msg="nope"
    if(msg == "nope"):
        html = ""
    else:
        html = "<p>Message: "+str(msg)+"</p>"
    html += """<html>   
<body>
<h3>Login</h3>
<form action="/do_login/" method="post"/>
<input placeholder="username" name="username"/><br>
<input type="password" placeholder="password" name="password"/><br>
<input type="submit"/>
</form><br><br><br>
<h3>Signup</h3>
<form action="/do_signup/" method="post"/>
<input placeholder="username" name="username"/><br>
<input type="password" placeholder="password" name="password"/><br>
<input type="email" placeholder="email" name="email"/><br>
<input placeholder="name" name="name"/><br>
<input placeholder="Role(monshi/patient)" name="role"/><br>
<input placeholder="clinic_id(only if you are monshi)" name="clinic_id"/><br>
<input type="submit"/>
</form><br><br><br>
<h3>Add Clinic</h3>
<form action="/do_add_clinic/" method="post"/>
<input placeholder="clinic_id" name="clinic_id"/><br>
<input type="email" placeholder="email" name="email"/><br>
<input placeholder="name" name="name"/><br>
<input placeholder="Address" name="address"/><br>
<input placeholder="phone number" name="phone_number"/><br>
<input placeholder="services" name="services"/><br>
<input type="submit"/>
</form>
</body>
</html>"""
    return HttpResponse(html)