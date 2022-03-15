from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets

from users.utils import CustomAuth, ApiResponse, get_current_user, update_cache
from .models import Note, Label
from .serializers import NoteSerializers, LabelSerializers

RC = settings.REDIS_CONFIG


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
        user = get_current_user(request)
        data['user'] = user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        update_cache(user.id, Note)
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

        update_cache(get_current_user(request).id, Note)

        return ApiResponse(data=serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, *args, **kwargs):
        res = super().destroy(request, *args, **kwargs)
        update_cache(get_current_user(request).id, Note)
        return ApiResponse(data=res.data, status=status.HTTP_204_NO_CONTENT)


class LabelViewSet(viewsets.ViewSet):
    permission_classes = (CustomAuth,)

    def list(self, request):
        queryset = Label.objects.all().order_by("pk")
        serializer = LabelSerializers(queryset, many=True)
        return ApiResponse(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = LabelSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return ApiResponse(data=serializer.data, status=status.HTTP_201_CREATED)


class LabelDetailViewSet(viewsets.ViewSet):
    permission_classes = (CustomAuth,)

    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(Label, pk=pk)
        serializer = LabelSerializers(queryset)
        return ApiResponse(data=serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        qs = get_object_or_404(Label, pk=pk)
        serializer = LabelSerializers(qs, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return ApiResponse(data=serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        qs = get_object_or_404(Label, pk=pk)
        qs.delete()
        return ApiResponse(status=status.HTTP_204_NO_CONTENT)
