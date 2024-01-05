from django.urls import path
from users import views


urlpatterns = [
    path('dashboard_admin',views.admin_dashboard,name='admin_dashboard'),
    path('dashboard_user',views.user_dashboard,name='user_dashboard'),
    path('profile/',views.user_profile,name='user_profile'),
    path('edit_prof_pic/',views.edit_profile_photo,name='edit_profile_photo'),
    path('view_prof_pic/',views.getProfilePhotoView,name='getProfilePhotoView'),
    path('remove_prof_pic/',views.removeprofilephoto,name='removeprofilephoto'),
    path('v_staffs/',views.view_staffs,name='view_staffs'),
    path('admin_add_job_get/<int:id>',views.admin_add_job_get,name='admin_add_job_get'),
    path('admin_add_job_post/<int:id>',views.admin_add_job_post,name='admin_add_job_post'),
    path('approve_user/<int:id>',views.approve_user,name='approve_user'),
    path('reject_user/<int:id>',views.reject_user,name='reject_user'),
    path('adm_view_tasks/',views.admin_view_tasks,name='admin_view_tasks'),
    path('v_assigned_pr/',views.view_assigned_projects,name='view_assigned_projects'),
    path('change_pass/',views.change_password,name='change_password'),



]