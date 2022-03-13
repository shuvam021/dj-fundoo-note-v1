import jwt
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.response import Response
from django.urls import reverse


def ApiResponse(data=None, status=None, msg=""):
    message_switcher = {200: "Data fetch successful", 201: "Create or Update successful", 204: "Delete successful",
                        404: "User doesn't exist"}
    mod_data = {'status': status, 'message': message_switcher.get(status) if len(msg) == 0 else msg, 'data': data}
    return Response(data=mod_data, status=status)


def gen_token(payload):
    return jwt.encode(payload, settings.JWT_KEY, algorithm=settings.JWT_ALGORITHMS)


def decode_token(token):
    return jwt.decode(token, settings.JWT_KEY, algorithms=settings.JWT_ALGORITHMS)


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
