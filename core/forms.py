from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.base_user import BaseUserManager
from .models import *


# from mpesa.models import PaymentTransaction


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = customer
        fields = ('phone_number',)

    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ensure your phone Number is in this '
                                                                                'format: 2547XXXXXXXX',
                                                                 'class': 'form-control',
                                                                 'size': '15',
                                                                 'minlength': '12',
                                                                 'max_length': '12',
                                                                 }))


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = customer
        fields = ('phone_number',)
