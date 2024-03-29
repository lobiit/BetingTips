from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import CustomUserCreationForm, CustomUserChangeForm


# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = customer
    list_display = ('phone_number', 'is_staff', 'is_active',)
    list_filter = ('phone_number', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('phone_number',)
    ordering = ('phone_number',)


class GameAdmin(admin.ModelAdmin):
    list_display = ['game_id', 'home_team', 'away_team', 'is_over', 'date']
    list_filter = ['date', 'is_over']
    search_fields = ['game_id', 'home_team', 'away_team']


class GroupAdmin(admin.ModelAdmin):
    list_display = ['title']


# Register your models here.

class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "amount", "isFinished",
                    "isSuccessFull", "trans_id", 'date_created', 'date_expired', 'is_deleted')
    list_filter = ('isSuccessFull', 'date_created', 'is_deleted')
    list_per_page = 30
    search_fields = ('phone_number',)


admin.site.register(Game, GameAdmin)
admin.site.register(customer, CustomUserAdmin)
admin.site.register(PaymentTransaction, PaymentTransactionAdmin)
admin.site.register(Wallet)
admin.site.register(Group, GroupAdmin)
