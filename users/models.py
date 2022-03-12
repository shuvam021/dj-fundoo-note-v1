from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save

from users.utils import gen_token, MailService


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


def user_post_save(sender, instance, created, *args, **kwargs):
    if created:
        try:
            token = gen_token({'id': instance.id})
            MailService.verify_mail(email=instance.email, token=token)
        except Exception as e:
            print(e)


post_save.connect(user_post_save, sender=UserProfile)
