import logging

from django.conf import settings
from django.contrib.auth import authenticate, hashers
from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView

from users.serializers import UserSerializer
from users.utils import ApiResponse, decode_token, gen_token, MailService

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
            return ApiResponse(data=serializer.data, status=status.HTTP_201_CREATED)
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
        try:
            qs = self.get_object(pk)
        except Exception as e:
            return ApiResponse(msg=e.__str__(), status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(qs)
        return ApiResponse(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """Update the user's details with matching pk value"""
        try:
            qs = self.get_object(pk)
        except Exception as e:
            return ApiResponse(msg=e.__str__(), status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(qs, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse(data=serializer.data, status=status.HTTP_201_CREATED)
        return ApiResponse(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Remove the user's details with matching pk value"""
        try:
            qs = self.get_object(pk)
        except Exception as e:
            return ApiResponse(msg=e.__str__(), status=status.HTTP_404_NOT_FOUND)
        qs.delete()
        return ApiResponse(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
def verify_token(request, token):
    try:
        payload = decode_token(token)
        obj = get_object_or_404(User, pk=int(payload.get('id')))
        if obj:
            obj.is_verified = True
            obj.save()
        return ApiResponse(data={"id": obj.id, "is_verified": obj.is_verified}, status=status.HTTP_202_ACCEPTED)
    except Exception as e:
        logger.exception(e.__str__())
        return ApiResponse(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_view(request):
    """
    User authentication view
    accept email id and password

    :param request:
    :return:
    """

    data = request.data
    try:
        user = authenticate(**data)
        if not user:
            raise ValidationError
        token = gen_token(payload={"id": user.id})
        response = {"token": token}
        settings.REDIS_CONFIG.set(token, user.id, settings.JWT_EXP_TIME)
        return ApiResponse(data=response, status=status.HTTP_202_ACCEPTED, msg='Login Successful')
    except ValidationError as e:
        logger.exception(e.__str__())
        return ApiResponse(status=status.HTTP_401_UNAUTHORIZED, msg="Authentication failed")
    except Exception as e:
        logger.exception(e.__str__())
        return ApiResponse(status=status.HTTP_400_BAD_REQUEST, msg=e.__str__())


@api_view(['POST'])
def forget_password(request):
    """
    1st step of password change procedure
    accept valid email id to send mail about next step of the procedure

    :param request:
    :return:
    """
    data = request.data
    user = User.objects.get(email=data.get('email'))

    if not user:
        logger.warning(f"{data.get('email')} not found")
        return ApiResponse(status=status.HTTP_404_NOT_FOUND)

    token = gen_token({'id': user.id})
    try:
        MailService.forget_password_mail(user.email, token)
        return ApiResponse(msg=f'Password change link sent to {user.email}')
    except Exception as e:
        logger.exception(e.__str__())
        return ApiResponse(msg=e.__str__(), status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def change_password(request, token):
    """
    2nd step of password change procedure
    accept password1, password2 in request.data()

    :param request:
    :param token: autogenerated value i.e. collected form email
    :return:
    """
    data = request.data
    if data.get('password1') != data.get('password2'):
        return ApiResponse(status=status.HTTP_400_BAD_REQUEST, msg="password1 and password2 must me equal")
    payload = decode_token(token)
    user = User.objects.get(pk=int(payload.get('id')))
    if not user:
        return ApiResponse(status=status.HTTP_404_NOT_FOUND)

    try:
        user.password = hashers.make_password(data.get('password1'))
        user.save()
        return ApiResponse(msg="password changed", status=status.HTTP_202_ACCEPTED)
    except Exception as e:
        return ApiResponse(msg=e.__str__(), status=status.HTTP_400_BAD_REQUEST)
