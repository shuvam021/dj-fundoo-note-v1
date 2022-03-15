from rest_framework import serializers
from .models import Note, Label


class NoteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'title', 'description', 'user')


class LabelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ('id', 'title', 'author', 'color', 'note')
