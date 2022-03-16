from dataclasses import fields
from django import forms
from .models import Projects,Profile,Comments
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ('title','description', 'link', "user",'image')
        widgets={
            'title':forms.TextInput(attrs={'class': 'form-control'}),
            'link':forms.TextInput(attrs={'class': 'form-control'}),
            'user':forms.TextInput(attrs={'class': 'form-control','value': ' ','id':'elder','type':'hidden'}),
            'description':forms.Textarea(attrs={'class': 'form-control'}),
        }
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        exclude = ['user','project_id']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']