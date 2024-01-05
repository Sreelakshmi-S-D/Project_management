from django.urls import path
from project import views


urlpatterns = [
    path('add_project/',views.add_projects,name='add_project'),
    path('check_project/', views.check_projects, name="check_project"),
    path('project/',views.projects,name='view_projects'),
    path('get_p_data/<int:id>',views.get_project_data,name='get_project_data'),
    path('edit_p/<int:id>',views.edit_project,name='edit_project'),
    path('delete_project/<int:id>',views.delete_projects,name='delete_projects'),
    path('pro_to_u/<int:id>',views.project_to_user,name='project_to_user'),
    path('check_user/',views.check_user,name='check_user'),
    path('v_project_team/<int:id>',views.view_project_team,name='view_project_team'),
    path('removeu_from_team/<int:id>',views.removeu_from_team,name='removeu_from_team'),

    path('add_list/',views.add_list,name='add_list'),
    path('check_list/', views.check_List, name="check_List"),
    path('view_list/',views.view_list,name='view_list'),
    path('get_list/<int:id>',views.get_list_data,name='get_list_data'),
    path('update_list/<int:id>',views.update_list,name='update_list'),
    path('delete_list/<int:id>',views.delete_list,name='delete_list'),


    path('add_task/',views.add_task,name='add_task'),
    path('view_task/',views.view_tasks,name='view_tasks'),
    path('get_list/',views.get_list,name='get_list'),
    path('delete_task/<int:id>',views.delete_task,name='delete_task'),
    path('get_task_data/<int:id>',views.get_task_data,name='get_task_data'),
    path('update_task/<int:id>',views.update_task,name='update_task'),
    path('task_filter/',views.task_filter,name='task_filter'),
#     path('sort_task/',views.sort_task,name='sort_task'),


    path('add_subtask/',views.add_subtask,name='add_subtask'),
    path('view_subtask/<int:id>',views.view_subtask,name='view_subtask'),
    path('delete_subtask/<int:id>',views.delete_subtask,name='delete_subtask'),
    path('get_subtask_data/<int:id>',views.get_subtask_data,name='get_subtask_data'),
    path('update_subtask/<int:id>',views.update_subtask,name='update_subtask'),


]