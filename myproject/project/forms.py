from django import forms
from .models import *
from accounts.models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['status']

        widgets={
            'project_title':forms.TextInput(attrs={
                'id':'projectname','name':'project','class':'form-control'
            }),
            'description':forms.Textarea(attrs={
                'cols':20 ,'rows':3,'class':'form-control'
            }),
            'create_date':DateInput(attrs={
                'class':'form-control'
            }),
            'due_date':DateInput(attrs={
                'class':'form-control'
            })
        }
    # user_field = forms.ModelMultipleChoiceField(queryset=User.objects.select_related().exclude(is_superuser=True), label="Select User")
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     # Populate choices for the author field with author names
    #     self.fields['user_field'].widget = forms.Select(choices=[(user_field.id, user_field.Fullname) for user_field in User.objects.all()])





class EditProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

        widgets={
            'project_title':forms.TextInput(attrs={
                'id':'projectname','name':'project','class':'form-control'
            }),
            'description':forms.Textarea(attrs={
                'cols':20 ,'rows':3,'class':'form-control','id':'p_description'
            }),
            'create_date':DateInput(attrs={
                'class':'form-control','id':'p_create_date'
            }),
            'due_date':DateInput(attrs={
                'class':'form-control','id':'p_due_date'
            }),
            'status':forms.Select(attrs={
                'class':'form-select','id':'p_status'
            })
        }
        


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['status']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            # Populate choices for the author field with author names
            self.fields['list'].widget = forms.Select(choices=[(list.id, list.title) for list in List.objects.all()])

        widgets={
            'description':forms.Textarea(attrs={
                'cols':20 ,'rows':3
            }),
            'create_date':DateInput(),
            'due_date':DateInput()
        }



        
# class SubTaskForm(forms.ModelForm):
#     class Meta:
#         model = SubTask
#         fields = '__all__'

#         def __init__(self, *args, **kwargs):
#             super().__init__(*args, **kwargs)

#             # Populate choices for the author field with author names
#             self.fields['task'].widget = forms.Select(choices=[(task.id, task.task_title) for task in Task.objects.all()])



class TaskFilterForm(forms.Form):
    category=forms.CharField(required=False,widget=forms.TextInput(attrs={ 'id': "category",'placeholder':'Enter Category','name':'category'})) 
    statusoftask=forms.ChoiceField(choices=STATUS,required=False,widget=forms.Select(attrs={'class': 'form-select-sm ', 'id': "stsselect",'name':'status_select'})) 
    taskfromdate=forms.DateField(
        label="From",
        widget=forms.DateInput(attrs={
            'class': 'form-control-sm',
            'id': 'taskFdate',
            'type':'date',
            'name':'fromdate'
        }),
        required=False  
    )
    tasktodate=forms.DateField(
        label="To",
        widget=forms.DateInput(attrs={
            'class': 'form-control-sm',
            'id': 'taskTdate',
            'required': False,
            'type':'date',
            'name':'todate'
        }),
        required=False  
    )