from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class UserProfile(AbstractUser):
    """Extend class Default User model with custom fields"""
    is_verified = models.BooleanField(default=False)
    mobile = models.CharField(max_length=13)
    email = models.EmailField(unique=True, max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'first_name', 'lastname', 'mobile']

    def __str__(self):
        return f"User({self.username})"
