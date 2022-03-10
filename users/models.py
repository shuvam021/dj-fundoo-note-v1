from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_save
from django.core.mail import send_mail
from django.conf import settings
import logging
logging.basicConfig(filename=settings.LOG_FILE, encoding='utf-8', level=logging.warning, format=FORMAT)
logger = logging.getLogger(__name__)


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


def user_post_save(sender, instance, *args, **kwargs):
    logger.warning(f"verification mail send to {instance.first_name} accessed")
    try:
        send_mail(
            'Verify Your Account',
            'Click this link to verify your account http://127.0.0.1:8000/{jwt}',
            settings.EMAIL_HOST, (instance.email,), fail_silently=False
        )
    except Exception as e:
        print(e)


pre_save.connect(user_post_save, sender=UserProfile)
