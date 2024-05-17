# coding=utf-8

import re

from django.db import models
from django.core.validators import MaxLengthValidator, RegexValidator, MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin, AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _("Usuário"), 
        max_length=30, 
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message=_("Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters."),
                code='invalid'
            )
        ],
        help_text=_("A username that will be used for identification and login on the platform."),
    )
    name = models.CharField(_("Nome"), max_length=100, blank=True)
    email = models.EmailField(_("E-mail"), unique=True)
    is_staff = models.BooleanField(_("Staff Status"), default=False)
    is_active = models.BooleanField(_("Status"), default=True)
    date_joined = models.DateTimeField(_("Data"), auto_now_add=True)
    role = models.CharField(_("Papel"), max_length=100, blank=True)
    institution = models.CharField(_("Instituição"), max_length=100, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_groups'  # Ensure this line is unique
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_permissions'  # Ensure this line is unique
    )
    
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.name or self.username

    def get_short_name(self):
        return self.name.split(" ")[0] if self.name else self.username

    def user_has_role(self, role):
        return self.role == role
