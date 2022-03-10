from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import hashers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        if validated_data.get('password'):
            instance.password = hashers.make_password(validated_data.get('password'))
        instance.save()
        return instance
