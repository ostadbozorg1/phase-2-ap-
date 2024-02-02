from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout
from authentication.models import UserModel, ClinicModel, Appointment
from datetime import datetime
from datetime import date


def panel(request):
    if 'username' not in request.session:
        return redirect('../login/')
    user = UserModel.objects.get(username=request.session['username'])
    msg = request.GET.get('msg', "nope")
    msg2 = msg.replace(" ","")
    if(msg2.isalpha() is not True):
        msg="nope"
    if(msg == "nope"):
        html = ""
    else:
        html = "<p>Message: "+str(msg)+"</p>"
    if(user.role == "patient"):
        
        html += """<html>   
    <body>
    <h1>Panel</h1><br>
    <a href="/panel/list_clinics"><button>List clinics</button></a><br><br>
    <a href="/panel/new_appointment"><button>New appointment</button></a><br><br>
    <a href="/panel/my_appointments"><button>My appointments</button></a><br><br>
    <a href="/panel/logout"><button>Logout</button></a>
    </body>
    </html>"""
    if(user.role == "monshi"):
        html = """<html>   
    <body>
    <h1>Panel</h1><br>

    <a href="/panel/pending_appointments"><button>Pending appointments</button></a><br><br>
    <a href="/panel/confirmed_appointments"><button>Confirmed appointments</button></a><br><br>
        <a href="/panel/canceled_appointments"><button>Canceled appointments</button></a><br><br>
    <a href="/panel/passed_appointments"><button>Passed appointments</button></a><br><br>
    
    <a href="/panel/logout"><button>Logout</button></a>
    </body>
    </html>"""
    return HttpResponse(html)


def new_appointment(request):
    if 'username' not in request.session:
        return redirect('../login/?msg=Please login')
    user = UserModel.objects.get(username=request.session['username'])
    if(user.role != "patient"):
        return redirect('../panel/?msg=Access Denied')
    
    html = """<html>   
<body>
<h1>Make New Appointment</h1>
<form action="/panel/make_new_appointment/" method="post"/>
<input placeholder="clinic id" name="clinic_id"/><br><br>
<input type="text" placeholder="Date(2024-10-24)" name="date"/><br><br>
<input type="submit"/>
</form><br><br><a href="../../panel">Return to panel</a>
</body>
</html>"""
    return HttpResponse(html)

def make_new_appointment(request):
    if 'username' not in request.session:
        return redirect('../login/?msg=Please login')
    user = UserModel.objects.get(username=request.session['username'])
    if(user.role != "patient"):
        return redirect('../panel/?msg=Access Denied')
    if request.method == 'POST':
        clinic_id = request.POST['clinic_id']
        date_string = request.POST['date']
        
        try:
            clinic = ClinicModel.objects.get(clinic_id=clinic_id)
        except:
            return redirect('../panel/?msg=Wrong clinic id')
        
        try:
            date = datetime.strptime(date_string, '%Y-%m-%d').date()
        except:
            return redirect('../panel/?msg=wrong date format')
        
        appointment = Appointment(clinic_id=clinic_id, date=date, user_id=request.session['username'], status="pending")
        appointment.save()
        return redirect('../my_appointments/?msg=Success')
    

def my_appointments(request):
    msg = request.GET.get('msg', "nope")
    msg2 = msg.replace(" ","")
    if(msg2.isalpha() is not True):
        msg="nope"
    if(msg == "nope"):
        html = ""
    else:
        html = "<p>Message: "+str(msg)+"</p>"
    if 'username' not in request.session:
        return redirect('../../login/?msg=Please login')
    user = UserModel.objects.get(username=request.session['username'])
    if(user.role != "patient"):
        return redirect('../panel/?msg=Access Denied')
    
    Appointments = Appointment.objects.filter(user_id=request.session['username'])
    html += '<table><tr><th>Date</th><th>Clinic ID</th><th>Status</th><th>Actions</th></tr>'

    # Add a row for each appointment
    for appointment in Appointments:
        html += f'<tr><td>{appointment.date}</td><td>{appointment.clinic_id}</td><td>{appointment.status}</td><td><a href="/panel/cancel_appointment/?id={appointment.id}">Cancel</a></td></tr>'

    # End of the HTML table
    html += '</table><br><br><a href="../../panel">Return to panel</a>'

    return HttpResponse(html)
    

def cancel_appointment(request):
    if 'username' not in request.session:
        return redirect('../my_appointments/?msg=Please login')
    appoint_id = request.GET.get('id', "nope")
    if appoint_id == "nope" :
        return redirect('../login/?msg=Haaaaa')
    try:
        appoint = Appointment.objects.get(id=appoint_id)
    except:
        return redirect('../my_appointments/?msg=Wrong appointment id')
    user = UserModel.objects.get(username=request.session['username'])
    if(appoint.user_id != user.username):
        if(user.role != "monshi" or user.clinic_id != appoint.clinic_id):
            return redirect('../my_appointments/')
    appoint.status = "canceled"
    appoint.save()
    if(user.role == "patient"):
        return redirect('../my_appointments/')
    return redirect('../pending_appointments/')

def approve_appointment(request):
    if 'username' not in request.session:
        return redirect('../my_appointments/?msg=Please login')
    appoint_id = request.GET.get('id', "nope")
    if appoint_id == "nope" :
        return redirect('../login/?msg=Haaaaaaaaaa')
    try:
        appoint = Appointment.objects.get(id=appoint_id)
    except:
        return redirect('../my_appointments/?msg=Wrong id')
    user = UserModel.objects.get(username=request.session['username'])
    if(user.role != "monshi" or user.clinic_id != appoint.clinic_id):
        return redirect('../panel/?msg=Access Denied')
    appoint.status = "approved"
    appoint.save()
    return redirect('../pending_appointments/?msg=Success')
def list_clinics(request):
    Clinics = ClinicModel.objects.all()
    html = '<h1>List of Clinics</h1><br><table><tr><th>Name</th><th>Clinic ID</th><th>Email</th><th>Address</th><th>Phone Number</th><th>Services</th></tr>'

    # Add a row for each appointment
    for clinic in Clinics:
        html += f'<tr><td>{clinic.name}</td><td>{clinic.clinic_id}</td><td>{clinic.email}</td><td>{clinic.address}</td><td>{clinic.phone_number}</td><td>{clinic.services}</td></tr>'

    # End of the HTML table
    html += '</table><br><br><a href="../../panel">Return to panel</a>'

    return HttpResponse(html)

def make_logout(request):
    logout(request)
    return redirect('../?msg=Bye')
