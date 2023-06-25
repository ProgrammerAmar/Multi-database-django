from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import connections


class UserRegistrationForm(UserCreationForm):


    ROLE_CHOICES = [
        ('backend', 'Backend Developer'),
        ('graphic', 'Graphic Designer'),
        ('frontend', 'Frontend Developer'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']


class UserEditForm(UserCreationForm):
    ROLE_CHOICES = [
        ('backend', 'Backend Developer'),
        ('graphic', 'Graphic Designer'),
        ('frontend', 'Frontend Developer'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user_id = self.instance.id if self.instance else None

        try:
            user = User.objects.exclude(id=user_id).get(username=username)
            raise forms.ValidationError('A user with that username already exists.')
        except User.DoesNotExist:
            return username

        
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']
        
