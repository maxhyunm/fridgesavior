from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from users.managers import CustomUserManager
from base.models import SoftDeleteModel


class User(AbstractUser, SoftDeleteModel):
    username = models.CharField(max_length=100)
    email = models.EmailField(_('email address'), unique=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    social_provider = models.CharField(null=True, blank=True, max_length=30)
    social_id = models.CharField(null=True, blank=True, max_length=30)
    social_detail = models.JSONField(default=dict)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'user'
