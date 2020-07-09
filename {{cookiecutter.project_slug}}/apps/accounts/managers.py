from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def _create_user(self, email: str, password: str, is_staff: bool = False, is_superuser: bool = False, **extra_fields) -> settings.AUTH_USER_MODEL:
        if not email:
            raise ValueError(_('Users must have a email address!'))
        email = self.normalize_email(email)
        user = self.model(email=email, is_active=True, is_staff=is_staff, is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str = None, **extra_fields) -> settings.AUTH_USER_MODEL:
        return self._create_user(email, password, is_staff=False, is_superuser=False, **extra_fields)

    def create_superuser(self, email: str, password: str = None, **extra_fields) -> settings.AUTH_USER_MODEL:
        return self._create_user(email, password, is_staff=True, is_superuser=True, **extra_fields)

