from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from accounts.models import *
from django.contrib.auth import authenticate,login,logout
from users.views import *
from django.contrib.auth.forms import PasswordChangeForm
from .utils import log_user_action
from django.contrib.auth.decorators import login_required
from django.contrib import messages



# Create your views here.


def index(request):
    return render(request,'accounts/index.html')



def user_register(request):
    if request.method == 'POST':
        name = request.POST['fullname']
        email = request.POST['emailid']
        phn = request.POST['phone']
        dob = request.POST['dob']
        password = request.POST['password']
        confirm_passsword = request.POST['confirm_password']

        if password == confirm_passsword:
            newpassword = password
        u=User.objects.create_user(Fullname=name,email=email,password=newpassword,phone=phn,dob=dob) 
        log_user_action(u,'New user signed up')
        return redirect(users_login)

    else:
        return render(request,'accounts/user_register.html')
    
def check_email(request):
    email = request.GET.get('email', None)
    x = User.objects.filter(email=email)
    if len(x) == 0:
        res = False
    else:
        res = True
    return JsonResponse({'status': res}, safe=False)


def users_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request,email=email,password=password)
        print(user)
        if user:
            login(request,user)
            request.session['u_id']=user.id
            if user.is_superuser == 1:
                log_user_action(request.user,'Logged In' )
                return redirect(admin_dashboard)
                
            elif user.is_superuser == 0 and user.is_staff == 1:
                log_user_action(request.user,'Logged In' )
                # return redirect(user_profile)
                # return HttpResponse("<script>alert('Login Successfull');window.location='/user/user_profile/'</script>")
                return redirect(user_dashboard)
            else:
                messages.error(request, 'Incorrect username or password')
                return redirect(users_login)


        else:
            messages.error(request, 'Invalid User')
            return redirect(users_login)
    else: 
        return render(request,'accounts/login.html')
    

@login_required(login_url='/u_login/')
def user_logout(request):
    log_user_action(request.user,'Logged Out' )
    logout(request)
    return redirect(index)
