from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
import re


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.endswith('@purdue.edu'):
            self.add_error('email', 'Only Purdue emails are allowed.')
            
        if User.objects.filter(email=email).exists():
            self.add_error('email',"This email address is already in use.")
        return email
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']
