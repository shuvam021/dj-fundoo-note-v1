import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView

from users.serializers import UserSerializer
from users.utils import ApiResponse

logging.basicConfig(filename=settings.LOG_FILE, encoding='utf-8', level=logging.warning,
                    format='%(levelname)s - [%(asctime)s] - %(message)s')

logger = logging.getLogger(__name__)


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
