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
    