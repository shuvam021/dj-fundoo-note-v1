from rest_framework import generics
from rest_framework import status

from users.utils import CustomAuth, ApiResponse, get_current_user
from .models import Note
from .serializers import NoteSerializers


# Create your views here.
class NoteListCreateNoteApiView(generics.ListCreateAPIView):
    serializer_class = NoteSerializers
    permission_classes = (CustomAuth,)

    def get_queryset(self):
        user = get_current_user(self.request)
        return Note.objects.filter(user__id=user.id)

    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        return ApiResponse(data=res.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = get_current_user(request).id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return ApiResponse(data=serializer.data, status=status.HTTP_201_CREATED)


class NoteRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializers
    permission_classes = (CustomAuth,)

    def get_queryset(self):
        user = get_current_user(self.request)
        return Note.objects.filter(user__id=user.id)

    def retrieve(self, request, *args, **kwargs):
        res = super().retrieve(request, *args, **kwargs)
        return ApiResponse(data=res.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        qs = self.get_queryset().get(pk=kwargs.get('pk'))
        data = request.data.copy()
        data['user'] = qs.user.id
        serializer = self.get_serializer(qs, data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return ApiResponse(data=serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, *args, **kwargs):
        res = super().destroy(request, *args, **kwargs)
        return ApiResponse(data=res.data, status=status.HTTP_204_NO_CONTENT)
