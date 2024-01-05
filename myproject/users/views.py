from django.shortcuts import render,redirect,get_list_or_404
from django.http import HttpResponse, JsonResponse
from accounts.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from django.core.serializers import serialize
from project.models import *
from django.contrib.auth.forms import PasswordChangeForm
from accounts.utils import *
from project.forms import *
from accounts.views import *




# # Create your views here.

@login_required(login_url='/u_login/')
def admin_dashboard(request):
    total_project = Project.objects.all().count()
    ongoing_project = Project.objects.filter(status='In Progress').count()
    finished_project = Project.objects.filter(status='Completed').count()
    x=UserActivityLog.objects.all().order_by('-timestamp')
    context = {
        'data':x,
        'total_p': total_project,
        'ongoing_p': ongoing_project,
        'finished_p': finished_project

    }

    return render(request,'users/admin_dashboard.html',context)


@login_required(login_url='/u_login/')
def user_dashboard(request):
    id=request.session['u_id']
    assigned_projects = Project_to_user.objects.filter(user_id=id).count()
    projects = Project_to_user.objects.filter(user_id=id)
    ongoing_projects=0
    finished_projects = 0

    for i in projects:
        if i.project.status == 'In progress':
            ongoing_projects=+1
        elif i.project.status == 'Completed':
            finished_projects+=1


    x=User.objects.get(id=request.session['u_id'])
    log=UserActivityLog.objects.filter(user=request.user).order_by('-timestamp')

    context={
        'user':x, 
        'data':log,
        'assiged_p': assigned_projects,
        'ongoing_p': ongoing_projects,
        'finished_p': finished_projects

    }

    return render(request,'users/user_dashboard.html',context)



@login_required(login_url='/u_login/')
def user_profile(request):
    x=User.objects.get(id=request.user.id)
    if request.method == 'POST':
        name = request.POST['fullname']
        email = request.POST['emailid']
        job = request.POST['job']
        phn = request.POST['phone']
        dob = request.POST['dob1']

        if dob:
        # Check if dob is a string, and if not, format it
            dob_str = dob if isinstance(dob, str) else dob.strftime('%Y-%m-%d')
        else:
            dob_str = None

        User.objects.filter(id=request.user.id).update(Fullname=name,email=email,job_type=job,phone=phn,dob=dob_str)
            
        if request.user.is_superuser == 1:
            messages.success(request, 'Profile updated')
            return redirect(user_profile)
        elif request.user.is_superuser == 0:
            messages.success(request, 'Profile updated')
            log_user_action(request.user,'Profile changed' )
            return redirect(user_profile)
    else:
        photo = ProfilePhotoUploadForm()
        context={
            'user':x,
            'data':photo
        }
        return render(request,'users/profile.html',context)


def edit_profile_photo(request):
    form = ProfilePhotoUploadForm(request.FILES,request.POST)
    print(form)
    if form.is_valid():
        profile_image = request.FILES.get('profile_image')
        try:
            user_profile = User.objects.get(id=request.session['u_id'])
            user_profile.photo = profile_image
            user_profile.save()
            log_user_action(user_profile,'Profile photo updated')

            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found'})
    else:
        return JsonResponse({'success': False})

def getProfilePhotoView(request):
    try:
        user_profile = User.objects.get(pk=request.session['u_id'])
        photo_url = user_profile.photo.url if user_profile.photo  else '/static/Login/images/default_profile.jpg'
        return JsonResponse({'photo': photo_url})
    except User.DoesNotExist:
        return JsonResponse({'photo': '/static/Login/images/default_profile.jpg'})



def removeprofilephoto(request):
    try:
        user = User.objects.get(id=request.session['u_id'])

        if user.photo:
            print('...')
            user.photo.delete()  # Remove the photo file from storage
            user.photo = 'None'    # Set the photo field to None
            user.save()
            print('22222',user.photo)
            log_user_action(user,'Profile photo deleted')
        return JsonResponse({'message': 'Profile photo removed successfully'})
    except User.DoesNotExist:
        return JsonResponse({'message': 'User not found'}, status=404)
    


@login_required(login_url='/u_login/')
def view_staffs(request):
    emp = User.objects.filter(status='not approved',is_superuser=0)
    apr_emp = User.objects.filter(status='Approved',is_staff=1)
    return render(request,'users/view_staffs.html',{'emp':emp,'apr_emp':apr_emp})


def approve_user(request,id):
    user = User.objects.filter(id=id)
    user.update(status='Approved',is_staff=1)
    return redirect(view_staffs)


def reject_user(request,id):
    user = User.objects.filter(id=id)
    user.update(status='Reject')
    return redirect(view_staffs)

def admin_add_job_get(request,id):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            try:
                user = User.objects.get(id=id)
                user_data = {
                    'name' : user.Fullname,
                    'email': user.email,
                    'phone': user.phone,
                    'dob': user.dob,
                }
            
                return JsonResponse(user_data)
            except user.DoesNotExist:
                return JsonResponse({'error': 'user not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    


def admin_add_job_post(request,id):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            
        if request.method == 'POST':
            try:
                name = request.POST['fullname']
                email = request.POST['emailid']
                job = request.POST['job']
                phn = request.POST['phone']
                dob = request.POST['dob']
                job = request.POST['job']
                user = User.objects.filter(id=id)
                user.update(Fullname=name,email=email,job_type=job,phone=phn,dob=dob)  
                return JsonResponse({'success': True})
            except User.DoesNotExist:
                errors = {'error': 'Project not found'}
                return JsonResponse(errors, status=404)
        else:
            return JsonResponse({'errors': errors}, status=400)
    else:
        return HttpResponse("<script>alert('something went wrong!');history.back();</script>")
    


@login_required(login_url='/u_login/')    
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST,user=request.user)
        print(form)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            if request.user.is_staff == 1 and request.user.is_superuser == 0:
                return redirect('user_logout')
            else:
                return redirect('user_logout')
        else:
            return redirect(change_password)
    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, 'users/change_password.html', {'form': form})
    

@login_required(login_url='/u_login/')
def admin_view_tasks(request):
    x=Task.objects.all()
    tform = TaskFilterForm() 
    return render(request,'users/admin_view_tasks.html',{'view':x,'tfill':tform})


@login_required(login_url='/u_login/')
def view_assigned_projects(request):
    x=Project_to_user.objects.filter(user_id=request.session['u_id'])
    return render(request,'users/view_assigned_projects.html',{'project':x})