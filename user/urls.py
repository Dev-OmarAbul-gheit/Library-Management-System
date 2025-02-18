from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterViewSet, LoginViewSet, RequestPasswordResetViewSet, ConfirmPasswordResetViewSet

router = DefaultRouter()
router.register(prefix='register', viewset=RegisterViewSet, basename='register')
router.register(prefix='login', viewset=LoginViewSet, basename='login')
router.register(prefix='password-reset/request', viewset=RequestPasswordResetViewSet, basename='request-password-reset')
router.register(prefix='password-reset/confirm', viewset=ConfirmPasswordResetViewSet, basename='confirm-password-reset')

urlpatterns = [
    path('', include(router.urls))
]