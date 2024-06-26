# coding=utf-8

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
from .forms import UserAdminCreationForm, UserAdminForm


class UserAdmin(BaseUserAdmin):

    add_form = UserAdminCreationForm
    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'group', 'password1', 'password2')
        }),
    )
    form = UserAdminForm
    fieldsets = (
        (None, {
            'fields': ('username', 'email')
        }),
        ('Basic Information', {
            'fields': ('name', 'last_login', 'institution')
        }),
        (
            'Permissions', {
                'fields': (
                    'is_active','is_staff', 'is_superuser', 'groups',
                    'user_permissions'
                )
            }
        ),
    )
    list_display = ['username', 'name', 'email', 'is_active', 'is_staff', 'date_joined']


#admin.site.register(User, UserAdmin)
