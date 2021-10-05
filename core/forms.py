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


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = customer
        fields = ('phone_number',)


# class MpesaForm1(forms.ModelForm):
#     amount = forms.DecimalField(required=True)
#
#     class Meta:
#         model = PaymentTransaction
#         fields = ('amount',)
#
#
# class MpesaForm2(forms.ModelForm):
#     phone_number = forms.CharField(required=True)
#
#     class Meta:
#         model = PaymentTransaction
#         fields = ('phone_number',)
#
#