from django.contrib.auth.hashers import make_password
from django.core.mail import BadHeaderError
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from templated_mail.mail import BaseEmailMessage
from .models import User, PasswordResetOTP
from .serializers import RegisterUserSerializer, LoginUserSerializer, CreateOTPSerializer, UpdateUserPassword, UserSerializer
from rest_framework.decorators import action
from django.core.mail import send_mail
from django.template.loader import render_to_string


class ResetPasswordViewSet(CreateModelMixin, GenericViewSet):
    queryset = PasswordResetOTP.objects.all()
    serializer_class = CreateOTPSerializer

    def create(self, request):
        serializer = CreateOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password_otp = serializer.save()

        body = render_to_string('emails/password-reset-email.html', password_otp)

        send_mail(
            subject='Password Reset Request',
            message=body,
            html_message=body,
            from_email='admin@system.com',
            recipient_list=[password_otp.user.email]
        )

        return Response({'message': 'Password reset email sent.'}, status=status.HTTP_200_OK)
    



class UserViewSet(GenericViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'register':
            return RegisterUserSerializer
        elif self.action =="login":
            return LoginUserSerializer
        elif self.action == "update_password":
            return UpdateUserPassword
        return UserSerializer

    def get_object(self, request):
        return request.user

    @action(detail=False, methods=["post"])
    def register(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=["post"])
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["patch"])
    def update_password(self, request):
        serializer = UpdateUserPassword(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Your password has been updated successfully.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_me(self, request):
        user = self.get_object(request)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["patch"])
    def update_me(self, request):
        user = self.get_object(request)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["delete"])
    def delete_me(self, request):
        user = self.get_object(request)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)