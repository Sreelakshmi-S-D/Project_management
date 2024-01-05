from django.db import models
from datetime import *
from accounts.models import *

# Create your models here.


STATUS=(
        ('Pending','Pending'),
        ('In progress','In progress'),
        ('Completed','Completed'),
        ('Overdue','Overdue'),

    )


class Project(models.Model):
   
    project_title = models.CharField(max_length=150,blank=False,null=False,verbose_name='Title')
    description = models.CharField(max_length=250,blank=False,null=False,verbose_name='Description')
    create_date = models.DateField(default=datetime.now(),blank=False,null=False)
    due_date = models.DateField(blank=True,null=False)
    status = models.CharField(max_length=25,choices=STATUS,default='Pending')



class Project_to_user(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)


class List(models.Model):
    title = models.CharField(max_length=50,blank=False,verbose_name='TITLE')
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    

    def __str__(self) -> str:
        return self.title


class Task(models.Model):  
    task_title = models.CharField(max_length=150,blank=False,null=False,verbose_name='Title')
    description = models.CharField(max_length=250,blank=False,null=False,verbose_name='Description')
    create_date = models.DateField(default=datetime.now(),blank=False,null=False)
    due_date = models.DateField(blank=True,null=False)
    status = models.CharField(max_length=25,choices=STATUS,default='Pending')
    list = models.ForeignKey(List,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)


class SubTask(models.Model):
    title = models.CharField(max_length=50,blank=False,verbose_name='TITLE')
    status = models.CharField(max_length=25,choices=STATUS,default='Pending')
    task = models.ForeignKey(Task,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
