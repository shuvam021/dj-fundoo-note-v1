import logging

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from users.serializers import UserSerializer, LoginSerializer, ChangePasswordSerializer
from users.utils import ApiResponse, decode_token, gen_token

# Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(settings.LOG_FORMAT)
file_handler = logging.FileHandler(settings.LOG_FILE)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

User = get_user_model()


# Create your views here.
class UserApiView(APIView):
    """User View class"""

    def get(self, request):
        """List all users"""
        qs = User.objects.all()
        serializer = UserSerializer(qs, many=True)
        return ApiResponse(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Save new users"""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse(data=serializer.data, status=status.HTTP_200_OK)
        return ApiResponse(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailsApiView(APIView):

    @staticmethod
    def get_object(pk):
        """
        Return a user with matching pk value.
        If pk value doesn't exist then raise a 404 not found error
        """
        logger.info("User() accessed")
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """Return a user with matching pk value"""
        qs = self.get_object(pk)
        serializer = UserSerializer(qs)
        return ApiResponse(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """Update the user's details with matching pk value"""
        qs = self.get_object(pk)
        serializer = UserSerializer(qs, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse(data=serializer.data, status=status.HTTP_201_CREATED)
        return ApiResponse(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Remove the user's details with matching pk value"""
        qs = self.get_object(pk)
        qs.delete()
        return ApiResponse(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def verify_token(request, token):
    try:
        payload = decode_token(token)
        obj = get_object_or_404(User, pk=int(payload.get('id')))
        if obj:
            obj.is_verified = True
            obj.save()
        return ApiResponse(status=status.HTTP_200_OK)
    except Exception as e:
        logger.exception(e.__str__())
        return ApiResponse(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        user = authenticate(**serializer.data)
        if user:
            token = gen_token(payload={"id": user.id})
            response = {"token": token}
            return ApiResponse(data=response, status=status.HTTP_202_ACCEPTED, msg='Login Successful')
        else:
            logger.info(request.data.get('email'))
            logger.warning("Wrong credential tried")
            return ApiResponse(status=status.HTTP_401_UNAUTHORIZED, msg="Wrong credential tried")

    logger.warning("Wrong input tried")
    return ApiResponse(status=status.HTTP_404_NOT_FOUND, msg="Wrong input tried")


@api_view(['POST'])
def forget_password(request):
    data = request.data
    user = User.objects.get(email=data.get('email'))
    if user:
        token = gen_token({'id': user.id})
        msg_sub = "Change your password"
        msg_body = f"Hii, {user.email}\n"
        msg_body += f"use this link to change your password\n"
        msg_body += f"http://{settings.DOMAIN_NAME}/change_password/{token}/"
        try:
            send_mail(msg_sub, msg_body, settings.EMAIL_HOST, [user.email], fail_silently=False)
            return ApiResponse(msg=f'Password change link sent to {user.email}')
        except Exception as e:
            logger.exception(e.__str__())
    else:
        logger.warning(f"{data.get('email')} not found")
        return ApiResponse(status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def change_password(request, token):
    payload = decode_token(token)
    user = get_object_or_404(User, pk=int(payload.get('id')))
    pre_password = user.password
    if user:
        serializer = ChangePasswordSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            post_password = user.password
            if pre_password == post_password:
                return ApiResponse(msg="password changed attempt failed", status=status.HTTP_400_BAD_REQUEST)
            return ApiResponse(msg="password changed", status=status.HTTP_202_ACCEPTED)
    return ApiResponse(status=status.HTTP_404_NOT_FOUND)
