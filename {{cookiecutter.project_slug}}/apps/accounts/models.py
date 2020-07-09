from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.managers import UserManager, UserActiveManager


class User(AbstractBaseUser, PermissionsMixin):
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)
    email = models.EmailField(_('e-mail'), unique=True)
    is_active = models.BooleanField(_('is active'), blank=True, default=True)
    is_delete = models.BooleanField(_('is delete'), blank=True, default=False)
    is_staff = models.BooleanField(_('is staff'), blank=True, default=False)
    first_name = models.CharField(_('first name'), max_length=128)
    last_name = models.CharField(_('last name'), max_length=128)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return self.email

    def delete(self, *args, **kwargs):
        self.is_delete = True
        self.save(update_fields=['is_delete'])
        return self
