from django.contrib.auth.hashers import make_password
from django.core.mail import BadHeaderError
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from templated_mail.mail import BaseEmailMessage
from .models import User, PasswordResetOTP
from .serializers import RegisterUserSerializer, LoginUserSerializer, CreateOTPSerializer, UpdateUserPassword


class RegisterViewSet(CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer


class LoginViewSet(CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = LoginUserSerializer


class RequestPasswordResetViewSet(CreateModelMixin, GenericViewSet):
    queryset = PasswordResetOTP.objects.all()
    serializer_class = CreateOTPSerializer

    def create(self, request):
        serializer = CreateOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        otp = data['otp']
        username = data['username']
        user_email = data['email']

        context = {
            'subject': 'Password Reset Request',
            'username' : username,
            'otp' : otp,
            'reset_link' : f'http://127.0.0.1:8000/api/password-reset/confirm/otp={otp}'
        }

        try:
            message = BaseEmailMessage(template_name='emails/password-reset-email.html', context=context)
            message.send(from_email='admin@system.com', to=[user_email])

        except BadHeaderError:
            return Response({'error': 'Invalid header found.'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': 'Password reset email sent.'}, status=status.HTTP_200_OK)
    

class ConfirmPasswordResetViewSet(CreateAPIView, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UpdateUserPassword

    def create(self, request):
        serializer = UpdateUserPassword(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Your password has been reset successfully.'}, status=status.HTTP_200_OK)