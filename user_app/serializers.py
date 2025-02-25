from django.utils import timezone
from django.db import transaction
from django.forms import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from djoser.serializers import UserCreateSerializer
from .models import User, PasswordResetOTP

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        
class TokenSerializer(serializers.Serializer):    
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


class RegisterUserSerializer(TokenSerializer, UserCreateSerializer):
    
    class Meta(UserCreateSerializer.Meta):
        fields = ['username', 'email', 'password', 'refresh_token', 'access_token']
        extra_kwargs = {
            'username': {'write_only': True},
            'email': {'write_only': True},
            'password': {'write_only': True},
        }

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(_('A user with the given username is already exists.'))
        return username

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(_('A user with the given email is already exists.'))
        return email

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return self.create_user_tokens(user)


class LoginUserSerializer(TokenSerializer, serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    def authenticate_user(self, credentials):
        email = credentials['email']
        password = credentials['password']
        if not(user := authenticate(email=email, password=password)):
            raise serializers.ValidationError(_('Invalid credentials'))
        else:
            return user

    def create(self, validated_data):
        user = self.authenticate_user(validated_data)
        return self.create_user_tokens(user)


class CreateOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

    def validate_email(self,email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(_('No user exists with the given email address.'))
        return email

    def create(self, validated_data):
        email = validated_data['email']
        user = User.objects.get(email=email)
        return PasswordResetOTP.objects.create(user=user)


class UpdateUserPasswordSerializer(serializers.Serializer):
    otp = serializers.CharField()
    new_password = serializers.CharField()

    def validate_otp(self, otp):
        if not PasswordResetOTP.objects.filter(otp=otp, expires_at__gt=timezone.now()).exists():
            raise serializers.ValidationError(_('Invalid or expired confirmation code.'))
        return otp
    
    def validate_new_password(self, new_password):
        try:
            validate_password(new_password)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return new_password
    
    def create(self, validated_data):
        otp = PasswordResetOTP.objects.get(otp=validated_data['otp'], expires_at__gt=timezone.now())

        with transaction.atomic():
            # Update the user's password
            user = otp.user
            user.password = make_password(validated_data['new_password'])
            user.save()
            self.instance = user

            # Delete the otp
            otp.delete()

        return self.instance