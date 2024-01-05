from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from users.models import *
from accounts.models import *
from accounts.utils import *
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import send_mail
from myproject import settings
from celery import shared_task
from django.utils import timezone



# Create your views here.


@login_required(login_url='/u_login/')
def add_projects(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            form=ProjectForm(request.POST)
            if form.is_valid():
                form.save()
                # messages.success(request, 'Project created Successfully')
                log_user_action(request.user,' created new project ')
                return JsonResponse({'message':'ok'})     
                    
            else:
                print(form.errors,"new error")
                errors = form.errors.as_json()
                return JsonResponse({'errors': errors}, status=400)
    else:
          
        return HttpResponse("<script>alert('something went wrong!');history.back();</script>")

    
@login_required(login_url='/u_login/')
def check_projects(request):
    project = request.GET.get('project', None)
    x = Project.objects.filter(project_title=project)
    if len(x) == 0:
        res = False
    else:
        res = True
    return JsonResponse({'status': res}, safe=False)
    
@login_required(login_url='/u_login/')
def projects(request):
    x=Project.objects.all().order_by('id')
    y=ProjectForm()
    z=EditProjectForm()
    return render(request,'project/projects.html',{'view':x,'form':y,'edit_p':z})

def get_project_data(request,id):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            try:
                project = Project.objects.get(id=id)
                project_data = {
                    'project_id' : project.id,
                    'projectname': project.project_title,
                    'description': project.description,
                    'startdate': project.create_date,
                    'enddate': project.due_date,
                    'status': project.status,
                }
            
                return JsonResponse(project_data)
            except Project.DoesNotExist:
                return JsonResponse({'error': 'Project not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    

@login_required(login_url='/u_login/')
def edit_project(request,id):

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':

        if request.method == 'POST':
            try:

                x=Project.objects.get(id=id)

                frm = EditProjectForm(request.POST,instance=x)
                if frm.is_valid():
                        frm.save()
                        return JsonResponse({'message':'ok'})
                else:
                    return JsonResponse({'errors': errors}, status=400)
            except Project.DoesNotExist:
                errors = {'error': 'Project not found'}
                return JsonResponse(errors, status=404)

    else:
        return HttpResponse("<script>alert('something went wrong!');history.back();</script>")

     


@login_required(login_url='/u_login/')
def delete_projects(request,id):
    x=Project.objects.get(id=id)
    x.delete()
    return redirect(projects)




@login_required(login_url='/u_login/')
def project_to_user(request,id):
    if request.method == 'POST':
    
        project = request.POST['project']
        user_ids = request.POST.getlist('users')
        email = []

        for user_id in user_ids:
            project_to_user_instance = Project_to_user.objects.create(user_id=user_id, project_id=id)
            email.append(project_to_user_instance.user.email)

        Project.objects.filter(id=id).update(status='In progress')

        subject = "Project"
        for user_id in user_ids:
            project_to_user_instance = Project_to_user.objects.get(user_id=user_id, project_id=id)
            msg = (
                f"project name: {project_to_user_instance.project.project_title}\n"
                f"details: {project_to_user_instance.project.description}\n"
                f"Due date: {project_to_user_instance.project.due_date}"
            )
            send_mail(subject, msg, settings.EMAIL_HOST_USER, [project_to_user_instance.user.email])

            return JsonResponse({'message':'ok'})
            
        
    else:
        project = Project.objects.get(id=id)
        users = User.objects.filter(is_superuser=0,is_staff=1)
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            try:
                
                user_data = [{
                    'id' : user.id,
                    'name': user.Fullname,
                    'email': user.email,
                }
                for user in users
                ]

                project_data = {
                    'project_id' : project.id,
                    'projectname': project.project_title,
                    'description': project.description,
                    'startdate': project.create_date,
                    'enddate': project.due_date,
                    'status': project.status,
                }

            
                return JsonResponse({'users':user_data,'project':project_data})
            except Project.DoesNotExist:
                return JsonResponse({'error': 'Project not found'}, status=404)
        else:
            return JsonResponse({'error': 'Invalid request'}, status=400)
            
        
    



def check_user(request):
    users = request.GET.getlist('users_id[]')
    project = request.GET.get('project')
    user_ids_as_int = [int(user_id) for user_id in users]
    users_name = []
    projectid=Project.objects.get(project_title=project)
    for user_id in user_ids_as_int:
        queryset = Project_to_user.objects.filter(user_id=user_id,project_id=projectid)
        
        for project_user in queryset:
            if project_user.user.Fullname in users_name:
                pass
            else:
                users_name.append(project_user.user.Fullname)



    # print(x)
    if users_name==[]:
        res = False
    else:
        res = True
    return JsonResponse({'status': res,'users_name':users_name}, safe=False) 


@login_required(login_url='/u_login/')
def view_project_team(request,id):
    x=Project_to_user.objects.filter(project_id=id)
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            try:
                team_data = [{
                    'user_id' : team.user.id,
                    'user_name': team.user.Fullname,
                }
                for team in x
                ]
                # print(team_data)
            
                return JsonResponse({'project_team':team_data})
            except Project.DoesNotExist:
                return JsonResponse({'error': 'Project not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    # return render(request,'manager/view_projectteam.html',{'team':x})


@login_required(login_url='/u_login/')
def removeu_from_team(request,id):
    user = Project_to_user.objects.filter(user_id=id)
    user.delete()
    return redirect(projects)




@login_required(login_url='/u_login/')
def add_list(request):
    if request.method == 'POST':
        list_title = request.POST['lst']
        pro = request.POST['project']
        List.objects.create(title=list_title,project_id=pro,user_id=request.session['u_id']).save()
        return JsonResponse({'message':'ok'})     
                

    else:    
        pro=Project_to_user.objects.filter(user_id=request.session['u_id'])
        # print(pro)
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                try:
                    project_data = [{
                        'project_id' : team.project.id,
                        'project_name': team.project.project_title,
                    }
                    for team in pro
                    ]
                    print(project_data)
                
                    return JsonResponse({'project':project_data})
                except Project.DoesNotExist:
                    return JsonResponse({'error': 'Project not found'}, status=404)
        else:
            return JsonResponse({'error': 'Invalid request'}, status=400)
        



@login_required(login_url='/u_login/')
def check_List(request):
    lst = request.GET.get('lst', None)
    project = request.GET.get('project', None)
    x = List.objects.filter(title=lst,project_id=project)
    print(x)
    if x:
        res = True
    else:
        res = False
    return JsonResponse({'status': res}, safe=False) 

@login_required(login_url='/u_login/')
def view_list(request):
    x=List.objects.filter(user_id=request.user.id)
    return render(request,'project/list.html',{'view':x})


@login_required(login_url='/u_login/')   
def delete_list(request,id):
    x=List.objects.get(id=id)
    x.delete()
    return redirect(view_list)  


@login_required(login_url='/u_login/')
def get_list_data(request,id):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            try:
                x=List.objects.get(id=id)
                project_data = {
                    'list_name': x.title,
                    'project_id': x.project_id,
                    'project_name': x.project.project_title,    
                }
            
                return JsonResponse(project_data)
            except Project.DoesNotExist:
                return JsonResponse({'error': 'Project not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


def update_list(request,id):   
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'POST':
            try:
                list_name = request.POST['list_name']
                List.objects.filter(id=id).update(title=list_name)
                return JsonResponse({'message':'ok'})
        
            except Project.DoesNotExist:
                errors = {'error': 'Project not found'}
                return JsonResponse(errors, status=404)

    else:
        return HttpResponse("<script>alert('something went wrong!');history.back();</script>")

@login_required(login_url='/u_login/')
def add_task(request):
    if request.method == 'POST':
        list_id = request.POST['lst']
        task = request.POST['task']
        description = request.POST['description']
        create_date = request.POST['create_date']
        due_date = request.POST['due_date']
        Task.objects.create(list_id=list_id,task_title=task,description=description,create_date=create_date,due_date=due_date,user_id=request.user.id)
        return JsonResponse({'message':'ok'})     
    else:  
        print('kposyh')
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            try:
                list_data = List.objects.filter(user_id=request.session['u_id']).values('id', 'title', 'project_id__id', 'project_id__project_title')

            
                unique_projects = set()  # To keep track of unique projects
                filtered_list_data = []

                for lst in list_data:
                    # Check if the project_id is unique
                    if lst['project_id__id'] not in unique_projects:
                        unique_projects.add(lst['project_id__id'])
                        filtered_list_data.append({
                            'list_id': lst['id'],
                            'list_name': lst['title'],
                            'project_id': lst['project_id__id'],
                            'project_name': lst['project_id__project_title']
                        })
                print(filtered_list_data)

                return JsonResponse({'list': filtered_list_data})

            except List.DoesNotExist:
                return JsonResponse({'error': 'List not found'}, status=404)

        else:
            return JsonResponse({'error': 'Invalid request'}, status=400)
        


@login_required(login_url='/u_login/')
def view_tasks(request):
    x=Task.objects.filter(user_id=request.user.id)
    tform = TaskFilterForm() 
    return render(request,'project/task.html',{'view':x,'tfill':tform})   



def get_list(request):
    try:
        val = request.GET.get('prj_id')
        
        data = List.objects.filter(project_id=val).values('id','title')    
        data_list = list(data)   
        print(data_list)  
        return JsonResponse({ 'data': data_list})
    except:
        return JsonResponse({'status': '0' , 'message': 'Some error occured'})
    
def delete_task(request,id):
    x=Task.objects.get(id=id)
    x.delete()
    return redirect(view_tasks)



@login_required(login_url='/u_login/')
def get_task_data(request,id):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            try:
                x=Task.objects.get(id=id)
                project_data = {
                    'task_id': x.id,
                    'task_name': x.task_title,
                    'description': x.description,
                    'start_date': x.create_date,    
                    'end_date': x.due_date,    

                }
            
                return JsonResponse(project_data)
            except Project.DoesNotExist:
                return JsonResponse({'error': 'Project not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    


def update_task(request,id):   
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'POST':
            try:
                
                task = request.POST['task']
                description = request.POST['description']
                due_date = request.POST['due_date']
                status = request.POST['status']
                print(status)
                Task.objects.filter(id=id).update(task_title=task,description=description,due_date=due_date,status=status)
                return JsonResponse({'message':'ok'})
        
            except Project.DoesNotExist:
                errors = {'error': 'Project not found'}
                return JsonResponse(errors, status=404)

    else:
        return HttpResponse("<script>alert('something went wrong!');history.back();</script>")
    

@login_required(login_url='/u_login/')
def add_subtask(request):
    if request.method == 'POST':
        subtask = request.POST['subtask']
        task = request.POST['a_task_h']
        SubTask.objects.create(title=subtask,task_id=task,user_id=request.user.id)
        return JsonResponse({'message':'ok'})  
    

def view_subtask(request,id):
    x=SubTask.objects.filter(task_id=id,user_id=request.user.id)
    return render(request,'project/subtask.html',{'sub_task':x})


def delete_subtask(request,id):
    x=SubTask.objects.get(id=id)
    x.delete()
    return redirect(view_subtask)


@login_required(login_url='/u_login/')
def get_subtask_data(request,id):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            try:
                x=SubTask.objects.get(id=id)
                subtask_data = {
                    'subtask_id': x.id,
                    'subtask_name': x.title,
                    'task_name':x.task.task_title

                }
            
                return JsonResponse(subtask_data)
            except Project.DoesNotExist:
                return JsonResponse({'error': 'Project not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    

def update_subtask(request,id):   
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'POST':
            try:   
                subtask = request.POST['e_subtask']
                status = request.POST['status']
                SubTask.objects.filter(id=id).update(title=subtask,status=status)
                return JsonResponse({'message':'ok'})
        
            except Project.DoesNotExist:
                errors = {'error': 'Project not found'}
                return JsonResponse(errors, status=404)

    else:
        return HttpResponse("<script>alert('something went wrong!');history.back();</script>")
    
@login_required(login_url='/u_login/')
def task_filter(request):
    if request.method == 'GET':
        category = request.GET.get('category', None)
        status = request.GET.get('statusoftask', None)
        from_date = request.GET.get('taskfromdate', None)
        to_date = request.GET.get('tasktodate', None)
        print(category)
        try:
            lst = List.objects.get(title=category)
            list_id = lst.id
        except List.DoesNotExist:
            category = False
        condition ={}

        if category:
            condition['list_id'] = list_id
              
        if status:
            
            condition['status'] = status
        

        if from_date and to_date:
            # Convert string dates to datetime objects
            from_date = datetime.strptime(from_date, '%Y-%m-%d')
            to_date = datetime.strptime(to_date, '%Y-%m-%d')

            # Use __range lookup to filter based on date range in due_date field
            condition['due_date__range'] = [from_date, to_date]

            # print('oooo',condition['due_date__range'])

        tasks = Task.objects.filter(**condition)

        project=[]
        list_name=[]
        for i in tasks:
            try:
                lst = List.objects.get(id=i.list_id)
                list_name.append(lst.title)
                project.append(lst.project.project_title)
            except List.DoesNotExist:
                i.list_id = False
      


        
        context = {
        'status': len(tasks) > 0,
        'filtered_data': list(tasks.values()),  # Serialize the queryset
        'project_name':project,
        'list_name':list_name
        }
     
       

        return JsonResponse(context, safe=False)
        
        
    return JsonResponse({'error': 'Invalid request method'}, status=400)



