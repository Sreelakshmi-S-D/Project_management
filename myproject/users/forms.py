from django import forms



class ProfilePhotoUploadForm(forms.Form):
    profile_image = forms.FileField(required=False,label='',widget=forms.FileInput(attrs={
        'style': 'display: none;', 
        'id':"profileImageInput", # Hide the file input
        'name':'profile_image'
    }))

    