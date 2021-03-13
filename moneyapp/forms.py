from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django import forms
from django.contrib.auth.models import User

class CreateUForm(UserCreationForm):
    # name = forms.CharField(max_length=200, null=True)
    # email =forms.CharField(max_length=200, null=True)
    # date_created = models.DateTimeField(auto_now_add=True, null=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
