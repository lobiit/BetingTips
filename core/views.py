from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login
from . import forms
import requests
import africastalking
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.contrib.auth.decorators import login_required
import json
from core.views import *
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from .LipaNaMpesaOnline import sendSTK, check_payment_status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from .models import PaymentTransaction
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
import datetime
import phonenumbers
from core.models import *


# Create your views here.
@login_required(login_url="/sign-in/")
def home(request):
    games = Game.objects.order_by('date').filter(is_over=True)
    group = Group.objects.filter(is_published=True)
    customers = customer.objects.all
    context = {
        'games': games,
        'group': group,
        'customer': customer
    }
    return render(request, 'index.html', context)


@login_required(login_url="/sign-in/")
def check(request):
    return render(request, 'CheckTransaction.html')




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
    if request.method == 'POST':
        current_customer = request.user
        transaction = PaymentTransaction.objects.filter(customer=current_customer, is_deleted=False).last()
        group = Group.objects.filter(is_published=True)
        check = request.POST['transaction_id']
        games = Game.objects.filter(is_over=False)

        context = {
            'transaction': transaction,
            'games': games,
            'group': group,
            'customer': customer.objects.all()
        }

        if check in transaction.trans_id:
            return render(request, 'profile.html', context)
        else:
            messages.error(request, "Ensure you entered the correct Transaction id")
            return redirect(reverse('check'))


# -*- coding: utf-8 -*-


import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from .LipaNaMpesaOnline import sendSTK, check_payment_status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from .models import PaymentTransaction
from django.http import JsonResponse
from rest_framework.permissions import AllowAny


# Create your views here.


class PaymentTranactionView(ListCreateAPIView):
    def post(self, request):
        return HttpResponse("OK", status=200)


# @login_required(login_url="/sign-in/")
class SubmitView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        customer = request.user
        # group = home.group
        data = request.data
        phone_number = data.get('phone_number')
        amount = data.get('amount')
        print(data.get('group_id'))
        group_id = int(data.get('group_id'))

        entity_id = 0
        if data.get('entity_id'):
            entity_id = data.get('entity_id')

        paybill_account_number = None
        if data.get('paybill_account_number'):
            paybill_account_number = data.get('paybill_account_number')

        transaction_id = sendSTK(customer, group_id, phone_number, amount, entity_id,
                                 account_number=paybill_account_number)

        # b2c()
        message = {"status": "ok", "transaction_id": transaction_id}
        return redirect(reverse('check'))
        # return Response(message, status=HTTP_200_OK)


# @login_required(login_url="/sign-in/")
class CheckTransactionOnline(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        trans_id = request.data['transaction_id']
        transaction = PaymentTransaction.objects.filter(id=trans_id).get()
        try:
            if transaction.checkoutRequestID:
                status_response = check_payment_status(transaction.checkoutRequestID)
            # return JsonResponse(
            # "status_response", "status"=200)
            # return redirect(reverse('profile') )
            else:
                return JsonResponse({
                    "message": "Server Error. Transaction not found",
                    "status": False
                }, status=400)
        except PaymentTransaction.DoesNotExist:
            return JsonResponse({
                "message": "Server Error. Transaction not found",
                "status": False
            },
                status=400)


# @login_required(login_url="/sign-in/")
class CheckTransaction(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        data = request.data
        trans_id = data['transaction_id']
        try:
            transaction = PaymentTransaction.objects.filter(id=trans_id).get()
            if transaction:
                return JsonResponse({
                    "message": "ok",
                    "finished": transaction.isFinished,
                    "successful": transaction.isSuccessFull
                },
                    status=200)
            else:
                # TODO : Edit order if no transaction is found
                return JsonResponse({
                    "message": "Error. Transaction not found",
                    "status": False
                },
                    status=400)
        except PaymentTransaction.DoesNotExist:
            return JsonResponse({
                "message": "Server Error. Transaction not found",
                "status": False
            },
                status=400)


# @login_required(login_url="/sign-in/")
class RetryTransaction(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        trans_id = request.data['transaction_id']
        try:
            transaction = PaymentTransaction.objects.filter(id=trans_id).get()
            if transaction and transaction.isSuccessFull:
                return JsonResponse({
                    "message": "ok",
                    "finished": transaction.isFinished,
                    "successful": transaction.isSuccessFull
                },
                    status=200)
            else:
                response = sendSTK(
                    phone_number=transaction.phone_number,
                    amount=transaction.amount,
                    orderId=transaction.order_id,
                    transaction_id=trans_id)
                return JsonResponse({
                    "message": "ok",
                    "transaction_id": response
                },
                    status=200)

        except PaymentTransaction.DoesNotExist:
            return JsonResponse({
                "message": "Error. Transaction not found",
                "status": False
            },
                status=400)


class ConfirmView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        print("======================>I was here")
        print(request.data)
        # save the data
        request_data = json.dumps(request.data)
        request_data = json.loads(request_data)
        body = request_data.get('Body')
        resultcode = body.get('stkCallback').get('ResultCode')
        message = {
            "ResultCode": 0,
            "ResultDesc": "The service was accepted successfully",
            "ThirdPartyTransID": "1237867865"
        }
        transaction = None

        # Perform your processing here e.g. print it out...
        if resultcode == 0:
            print('Payment successful')
            requestId = body.get('stkCallback').get('CheckoutRequestID')
            metadata = body.get('stkCallback').get('CallbackMetadata').get('Item')
            for data in metadata:
                if data.get('Name') == "MpesaReceiptNumber":
                    receipt_number = data.get('Value')
            try:
                transaction = PaymentTransaction.objects.get(
                    checkoutRequestID=requestId)
            except:
                return Response(message, status=HTTP_200_OK)

            if transaction:
                transaction.trans_id = receipt_number
                transaction.isFinished = True
                transaction.isSuccessFull = True
                transaction.save()
                # return redirect(reverse('profile') )

            else:

                return Response(message, status=HTTP_200_OK)



        else:
            print('unsuccessfull')
            requestId = body.get('stkCallback').get('CheckoutRequestID')
            try:
                transaction = PaymentTransaction.objects.get(
                    checkoutRequestID=requestId)

            except:
                return Response(message, status=HTTP_200_OK)
            if transaction:
                transaction.isFinished = True
                transaction.isSuccessFull = False
                transaction.save()
                # return redirect(reverse('profile') )

        # Prepare the response, assuming no errors have occurred. Any response
        # other than a 0 (zero) for the 'ResultCode' during Validation only means
        # an error occurred and the transaction is cancelled

        # Send the response back to the server
        # return redirect(reverse('profile') )
        return Response(message, status=HTTP_200_OK)

    def get(self, request):
        # return redirect(reverse('check') )
        return Response("Confirm callback", status=HTTP_200_OK)


class ValidateView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        # save the data
        request_data = request.data

        # Perform your processing here e.g. print it out...
        print("validate data" + request_data)

        # Prepare the response, assuming no errors have occurred. Any response
        # other than a 0 (zero) for the 'ResultCode' during Validation only means
        # an error occurred and the transaction is cancelled
        message = {
            "ResultCode": 0,
            "ResultDesc": "The service was accepted successfully",
            "ThirdPartyTransID": "1234567890"
        }

        # Send the response back to the server
        return Response(message, status=HTTP_200_OK)
