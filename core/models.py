from __future__ import unicode_literals

import uuid
from django.contrib.auth.models import User
from django.conf import settings

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.utils import timezone
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import datetime
import phonenumbers


# Create your models here.

class customer(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(_('Phone Number'), max_length=100, unique=True)
    email = models.EmailField(max_length=200, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self, phone_number=None):
        phonenumbers.format_number(phone_number, phonenumbers.PhoneNumber())
        u'111222333333'

        return self.phone_number


class Group(models.Model):
    title = models.CharField(max_length=100)
    amount = models.CharField(max_length=10)
    number_of_games = models.IntegerField()
    days = models.IntegerField(default=1)
    is_published = models.BooleanField(default=True)
    odds = models.CharField(max_length=100, default=14)

    def __str__(self):
        return self.title


class Game(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    number = models.IntegerField()
    game_id = models.AutoField(primary_key=True)
    home_team = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)
    tip = models.CharField(max_length=20)
    odds = models.FloatField(max_length=20, default=1.0)
    date = models.DateTimeField(default=timezone.datetime.today)
    time = models.DateTimeField(default=timezone.now)
    results = models.CharField(max_length=100, blank=True)
    won = models.BooleanField(default=True)
    is_over = models.BooleanField(default=False)


# -*- coding: utf-8 -*-


# Create your models here.
class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, blank=True)
    is_deleted = models.BooleanField(default=False, blank=True)

    class Meta:
        abstract = True


class PaymentTransaction(models.Model):
    customer = models.ForeignKey(customer, on_delete=models.CASCADE, null=True)
    phone_number = models.CharField(max_length=30)
    amount = models.DecimalField(('amount'), max_digits=6, decimal_places=2, default=0)
    isFinished = models.BooleanField(default=False)
    isSuccessFull = models.BooleanField(default=False)
    trans_id = models.CharField(max_length=30)
    order_id = models.CharField(max_length=200)
    checkoutRequestID = models.CharField(max_length=100)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, null=True)
    is_deleted = models.BooleanField(default=False)
    date_expired = models.DateTimeField(null=True)

    def __str__(self):
        return "{} {}".format(self.phone_number, self.amount)


class Wallet(BaseModel):
    phone_number = models.CharField(max_length=30)
    available_balance = models.DecimalField(('available_balance'), max_digits=6, decimal_places=2, default=0)
    actual_balance = models.DecimalField(('actual_balance'), max_digits=6, decimal_places=2, default=0)
    date_modified = models.DateTimeField(auto_now=True, null=True)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

    def __str__(self):
        return self.phone_number
