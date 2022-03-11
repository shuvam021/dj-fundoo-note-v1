from django.contrib.auth import get_user_model
from django.contrib.auth import hashers
from rest_framework import serializers

User = get_user_model()


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


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128)


class ChangePasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(max_length=128)
    password2 = serializers.CharField(max_length=128)

    def update(self, instance, validated_data):
        if validated_data.get('password1') != validated_data.get('password2'):
            raise ValueError("password1 and password2 must me equal")
        instance.password = hashers.make_password(validated_data.get('password1'))
        instance.save()
        return instance
