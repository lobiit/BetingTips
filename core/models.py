import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.utils import timezone
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import datetime


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

    def __str__(self):
        return self.phone_number


class Game(models.Model):
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
