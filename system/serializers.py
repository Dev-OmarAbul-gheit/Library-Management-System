from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User

class UserSerializer(serializers.Serializer):    
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    refresh_token = serializers.CharField(read_only=True)
    access_token = serializers.CharField(read_only=True)

    def create_user_tokens(self, user):
        """
        This function is used to create the (refresh_token) and (access_token),
        for the given user.
        """
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        return {'refresh_token' : str(refresh_token), 'access_token' : str(access_token)}


class RegisterUserSerializer(UserSerializer, UserCreateSerializer):
    username = serializers.CharField(write_only=True)
    
    class Meta(UserCreateSerializer.Meta):
        fields = ['username', 'email', 'password', 'refresh_token', 'access_token']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        tokens = self.create_user_tokens(user)
        return {'user': user, **tokens}


class LoginUserSerializer(UserSerializer, serializers.Serializer):
    def authenticate_user(self, credentials):
        email = credentials['email']
        password = credentials['password']
        if not(user := authenticate(email=email, password=password)):
            raise serializers.ValidationError('Invalid credentials')
        else:
            return user

    def create(self, validated_data):
        user = self.authenticate_user(validated_data)
        return self.create_user_tokens(user)