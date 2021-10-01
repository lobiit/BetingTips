from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from . import forms
import requests
import africastalking
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.conf import settings

from core.models import *


# Create your views here.
def home(request):
    return render(request, 'index.html')



def sign_in(request):
    username = request.POST['phone_number']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
    else:
        # Return an 'invalid login' error message.
        ...


def sign_up(request):
    form = forms.CustomUserCreationForm()

    if request.method == 'POST':
        form = forms.CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            user.save()

            # login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')

    return render(request, 'sign_up.html', {
        'form': form
    })


@login_required(login_url="/sign-in/")
def profile_page(request):
    password_form = PasswordChangeForm(request.user)

    if request.method == "POST":

        if request.POST.get('action') == 'update_password':
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)

                messages.success(request, 'Your password has been updated')
                return redirect(reverse('profile'))

            request.user.save()
            return redirect(reverse('profile'))

    return render(request, 'profile.html', {
        "password_form": password_form
    })

## Initialize SDK
#username = 'sandbox'
#api_key = "a848a8aaeb268d06fbdd443fd8d8ec344edf920958b2443b5a7e9a68dd6ecdef"
#africastalking.initialize(username,api_key)
#var = africastalking.Payment
## Initialize a service e.g. SMS
#sms = africastalking.SMS

## Use the service synchronously
#response = sms.send("Hello Message!", [customer.phone_number])
#print(response)
