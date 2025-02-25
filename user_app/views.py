from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .models import User
from .serializers import (
    UserSerializer,
    RegisterUserSerializer,
    LoginUserSerializer,
    CreateOTPSerializer,
    UpdateUserPasswordSerializer,
)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action == "register":
            return RegisterUserSerializer
        elif self.action == "login":
            return LoginUserSerializer
        elif self.action == "request_password_reset":
            return CreateOTPSerializer
        elif self.action == "confirm_password_reset":
            return UpdateUserPasswordSerializer
        return UserSerializer

    def get_object(self):
        return self.request.user

    @action(
        detail=False,
        methods=["POST"],
        url_path="register",
        url_name="user-registeration",
        permission_classes=[AllowAny],
    )
    def register(self, request):
        return super().create(request)

    @action(
        detail=False,
        methods=["POST"],
        url_path="login",
        url_name="user-login",
        permission_classes=[AllowAny],
    )
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["GET"],
        url_path="me",
        url_name="get-user",
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        return super().retrieve(request)

    @action(
        detail=False,
        methods=["POST"],
        url_path="password-reset/request",
        url_name="request-password-reset",
        permission_classes=[AllowAny],
    )
    def request_password_reset(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                _("message"): _(
                    "We have sent password reset email with confirmation code to you."
                )
            },
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=["POST"],
        url_path="password-reset/confirm",
        url_name="confirm-password-reset",
        permission_classes=[AllowAny],
    )
    def confirm_password_reset(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {_("message"): _("Your password has been reset successfully.")},
            status=status.HTTP_200_OK,
        )
