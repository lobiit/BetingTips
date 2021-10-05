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


# Create your models here.

# class Membership(models.Model):
#     MEMBERSHIP_CHOICES = (
#         ('Daily', 'daily'),
#         ('Weekly', 'weekly'),
#         ('HT/FT', 'ht/ft'),
#         ('Correct', 'correct'),
#         ('Sportpesa_Midweek', 'sportpesa_midweek'),
#         ('Sportpesa_Mega', 'sportpesa_mega'),
#         ('Betika_Midweek', 'betika_midweek'),
#         ('Betika_Mega', 'betika_mega'),
#     )
#     slug = models.SlugField(null=True, blank=True)
#     membership_type = models.CharField(
#         choices=MEMBERSHIP_CHOICES, default='Daily',
#         max_length=30
#     )
#     price = models.DecimalField(default=0)
#
#     def __str__(self):
#         return self.membership_type

class customer(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(_('Phone Number'), max_length=100, unique=True)
    email = models.EmailField(max_length=200, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    # membership = models.ForeignKey(Membership, related_name='user_membership', on_delete=models.SET_NULL, null=True)
    # membership = models.CharField(max_length=100, null=True)
    # id = models.AutoField(primary_key=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number


class Group(models.Model):
    title = models.CharField(max_length=100)
    amount = models.CharField(max_length=10)
    number = models.IntegerField()
    is_published = models.BooleanField(default=True)

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

#
# class Subscription(models.Model):
#     user_membership = models.ForeignKey(customer, related_name='subscription', on_delete=models.CASCADE)
#     active = models.BooleanField(default=True)
#
#     def __str__(self):
#         return self.user_membership.user.username
