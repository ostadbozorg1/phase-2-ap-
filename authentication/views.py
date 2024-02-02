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
        print("ummmm")
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
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 0;
      background-color: #f4f4f4;
    }

    form {
      max-width: 300px;
      margin: 0 auto;
      background: #fff;
      padding: 20px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
      border-radius: 5px;
    }

    input {
      display: block;
      width: calc(100% - 22px);
      padding: 10px;
      margin: 10px 0;
      border: 1px solid #ccc;
      border-radius: 3px;
      box-sizing: border-box;
      font-size: 16px;
    }

    input[type="submit"] {
      background: #4CAF50;
      color: #fff;
      border: none;
      cursor: pointer;
    }

    h3 {
      text-align: center;
      margin-bottom: 20px;
    }
  </style>
</head>
<body>
  <form action="/do_login/" method="post">
    <h3>Login</h3>
    <input type="text" placeholder="Username" name="username">
    <input type="password" placeholder="Password" name="password">
    <input type="submit" value="Login">
  </form>

<form action="/do_signup/" method="post">
    <h3>Signup</h3>
    <input type="text" placeholder="Username" name="username">
    <input type="password" placeholder="Password" name="password">
    <input type="email" placeholder="Email" name="email">
    <input type="text" placeholder="Name" name="name">
     

    
     
    <input type="text" placeholder="Clinic ID (only if you are monshi)" name="clinic_id">

    <input type="radio" id="monshi" name="role" value="monshi">
    <label for="monshi">Monshi</label>
     
    <input type="radio" id="patient" name="role" value="patient">
    <label for="patient">Patient</label>
    <input type="submit" value="Signup">
     
  </form>

  <form action="/do_add_clinic/" method="post">
    <h3>Add Clinic</h3>
    <input type="text" placeholder="Clinic ID" name="clinic_id">
    <input type="email" placeholder="Email" name="email">
    <input type="text" placeholder="Name" name="name">
    <input type="text" placeholder="Address" name="address">
    <input type="text" placeholder="Phone Number" name="phone_number">
    <input type="text" placeholder="Services" name="services">
    <input type="submit" value="Add Clinic">
  </form>
</body>
</html>"""
    return HttpResponse(html)