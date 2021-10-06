import os, socket, json, requests, datetime
from django.shortcuts import render, redirect
from django.urls import reverse
import requests
from django.contrib.auth.decorators import login_required
from requests.auth import HTTPBasicAuth
from base64 import b64encode
from .models import PaymentTransaction
from BetTip.settings import api_settings
from core.views import *
from django.contrib import messages

# Read variables from settings file

consumer_key = api_settings.CONSUMER_KEY
consumer_secret = api_settings.CONSUMER_SECRET

HOST_NAME = api_settings.HOST_NAME
PASS_KEY = api_settings.PASS_KEY
SHORT_CODE = api_settings.SHORT_CODE
SAFARICOM_API = api_settings.SAFARICOM_API

from rest_framework import serializers


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction


# Applies for LipaNaMpesaOnline Payment method
def generate_pass_key():
    time_now = datetime.datetime.now().strftime("%Y%m%d%H%I%S")
    s = SHORT_CODE + PASS_KEY + time_now
    encoded = b64encode(s.encode('utf-8')).decode('utf-8')


def get_token():
    api_url = "{}/oauth/v1/generate?grant_type=client_credentials".format(SAFARICOM_API)

    r = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    if r.status_code == 200:
        jonresponse = json.loads(r.content)
        access_token = jonresponse['access_token']
        return access_token
    elif r.status_code == 400:
        print('Invalid credentials.')
        return False


def sendSTK(phone_number, amount, orderId=0, transaction_id=None, shortcode=None, account_number=None):
    code = shortcode or SHORT_CODE
    access_token = get_token()
    if access_token is False:
        raise Exception("Invalid Consumer key or secret or both")

    time_now = datetime.datetime.now().strftime("%Y%m%d%H%I%S")

    s = code + PASS_KEY + time_now
    encoded = b64encode(s.encode('utf-8')).decode('utf-8')

    api_url = "{}/mpesa/stkpush/v1/processrequest".format(SAFARICOM_API)
    headers = {
        "Authorization": "Bearer %s" % access_token,
        "Content-Type": "application/json",
    }

    transaction_type = "CustomerBuyGoodsOnline"
    # If account number is set, change transaction type to paybill
    if account_number:
        transaction_type = "CustomerPayBillOnline"
    print("==========================================>")
    print(amount)

    request = {
        "BusinessShortCode": code,
        "Password": encoded,
        "Timestamp": time_now,
        "TransactionType": transaction_type,
        "Amount": str(int(amount)),
        "PartyA": phone_number,
        "PartyB": code,
        "PhoneNumber": phone_number,
        # "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "CallBackURL": "{}/confirm/".format(HOST_NAME),
        "AccountReference": account_number or code,
        "TransactionDesc": "{}".format(phone_number)
    }

    print(request)
    response = requests.post(api_url, json=request, headers=headers)
    json_response = json.loads(response.text)
    if json_response.get('ResponseCode'):
        if json_response["ResponseCode"] == "0":
            checkout_id = json_response["CheckoutRequestID"]
            if transaction_id:
                transaction = PaymentTransaction.objects.filter(id=transaction_id)
                transaction.checkoutRequestID = checkout_id

                transaction.save()
                return transaction.id
                # return render(request, 'profile.html')
                # return redirect(reverse('profile') )
            else:

                transaction = PaymentTransaction.objects.create(phone_number=phone_number,
                                                                checkoutRequestID=checkout_id,
                                                                amount=amount, order_id=orderId)

                transaction.save()

                return transaction.id
                # return render(request, 'profile.html')
                # return redirect(reverse('profile') )
    else:
        raise Exception("Error sending MPesa stk push", json_response)

    #return redirect(reverse('profile'))


def check_payment_status(checkout_request_id, shortcode=None):
    code = shortcode or SHORT_CODE
    access_token = get_token()
    time_now = datetime.datetime.now().strftime("%Y%m%d%H%I%S")

    s = code + PASS_KEY + time_now
    encoded = b64encode(s.encode('utf-8')).decode('utf-8')

    api_url = "{}/stkpushquery/v1/query".format(SAFARICOM_API)
    headers = {
        "Authorization": "Bearer %s" % access_token,
        "Content-Type": "application/json",
    }
    request = {
        "BusinessShortCode": code,
        "Password": encoded,
        "Timestamp": time_now,
        "CheckoutRequestID": checkout_request_id
    }
    response = requests.post(api_url, json=request, headers=headers)
    json_response = json.loads(response.text)
    if 'ResponseCode' in json_response and json_response["ResponseCode"] == "0":
        requestId = json_response.get('CheckoutRequestID')
        transaction = PaymentTransaction.objects.get(
            checkoutRequestID=requestId)
        if transaction:
            transaction.isFinished = True
            transaction.isSuccessFull = True
            transaction.save()
            return redirect(reverse('profile'))

        else:
            return redirect(reverse('/'))

        result_code = json_response['ResultCode']
        response_message = json_response['ResultDesc']
        return {
            "result_code": result_code,
            "status": result_code == "0",
            "message": response_message
        }

    else:
        raise Exception("Error sending MPesa stk push", json_response)
