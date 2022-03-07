from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager)
from django.db import models

# custom Authentication Models
# Create your models here.
# class UserManager(BaseUserManager):
#     def create_user(self, email, username, first_name, password, **other_fields):
#         if not email:
#             raise ValueError('You must provide an email address')
#         email = self.normalize_email(email)
#         user = self.model(
#             email=email,
#             username=username,
#             first_name=first_name,
#             **other_fields
#         )
#         user.set_password(password)
#         user.save()
#         return user
#
#     def create_superuser(self, email, username, first_name, password, **other_fields):
#         other_fields.setdefault('is_staff', True)
#         other_fields.setdefault('is_superuser', True)
#         other_fields.setdefault('is_active', True)
#         if not other_fields.get('is_staff'):
#             raise ValueError('Superuser must be assigned to is_staff=True.')
#         if not other_fields.get('is_superuser'):
#             raise ValueError('Superuser must be assigned to is_superuser=True.')
#         return self.create_user(email, username, first_name, password, **other_fields)
#
#
# class User(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     username = models.CharField(max_length=150, unique=True)
#     first_name = models.CharField(max_length=150, blank=True)
#     last_name = models.CharField(max_length=150, blank=True)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=False)
#
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['username', 'email']
#
#     def __str__(self):
#         return f"User({self.username})"
