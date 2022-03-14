from rest_framework import generics
from rest_framework import status

from users.utils import CustomAuth, ApiResponse
from .models import Note
from .serializers import NoteSerializers


# Create your views here.
class NoteListCreateNoteApiView(generics.ListCreateAPIView):
    serializer_class = NoteSerializers
    queryset = Note.objects.all()
    permission_classes = (CustomAuth,)

    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        return ApiResponse(data=res.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        res = super().create(request, *args, **kwargs)
        return ApiResponse(data=res.data, status=status.HTTP_201_CREATED)


class NoteRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializers
    queryset = Note.objects.all()
    permission_classes = (CustomAuth,)

    def retrieve(self, request, *args, **kwargs):
        res = super().retrieve(request, *args, **kwargs)
        return ApiResponse(data=res.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        res = super().update(request, *args, **kwargs)
        return ApiResponse(data=res.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, *args, **kwargs):
        res = super().destroy(request, *args, **kwargs)
        return ApiResponse(data=res.data, status=status.HTTP_204_NO_CONTENT)
