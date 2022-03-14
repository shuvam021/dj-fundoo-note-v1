import datetime
import logging

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

# Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(settings.LOG_FORMAT)
file_handler = logging.FileHandler(settings.LOG_FILE)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def ApiResponse(data=None, status=None, msg=""):
    message_switcher = {200: "Data fetch successful", 201: "Create or Update successful", 204: "Delete successful",
                        404: "User doesn't exist"}
    mod_data = {'status': status, 'message': message_switcher.get(status) if len(msg) == 0 else msg, 'data': data}
    return Response(data=mod_data, status=status)


def gen_token(payload):
    payload.update({"exp": datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(seconds=settings.JWT_EXP_TIME)})
    return jwt.encode(payload, settings.JWT_KEY, algorithm=settings.JWT_ALGORITHMS)


def decode_token(token):
    return jwt.decode(token, settings.JWT_KEY, algorithms=settings.JWT_ALGORITHMS, options={"verify_exp": True},)


class MailService:
    @staticmethod
    def verify_mail(email, token):
        msg_sub = "Verify Your Account"
        msg_body = f"Hii {email}\n"
        msg_body += f"Click this link to verify your account\n"
        msg_body += f"{settings.DOMAIN_NAME + reverse('verify_user', kwargs={'token': token})}"
        send_mail(msg_sub, msg_body, settings.EMAIL_HOST, [email], fail_silently=False)

    @staticmethod
    def forget_password_mail(email, token):
        msg_sub = "Change your password"
        msg_body = f"Hii, {email}\n"
        msg_body += f"use this link to change your password\n"
        msg_body += f"{settings.DOMAIN_NAME + reverse('change_password', kwargs={'token': token})}/"
        send_mail(msg_sub, msg_body, settings.EMAIL_HOST, [email], fail_silently=False)


class CustomAuth(BasePermission):
    def has_permission(self, request, view):
        auth_token = request.META.get('HTTP_AUTHORIZATION', None)
        pk = -1
        try:
            if auth_token:
                pk = decode_token(auth_token.split(' ')[1]).get('id')
        except jwt.ExpiredSignatureError as e:
            logger.exception(e.__str__())

        user = get_user_model().objects.filter(pk=pk)
        if user.exists():
            return True
        return False

    # def has_object_permission(self, request, view, obj):
    #     auth_token = request.META.get('HTTP_AUTHORIZATION', None)
    #     res = settings.REDIS_CONFIG.get(auth_token.split(' ')[1])
    #     if res:
    #         return True
    #     return False
