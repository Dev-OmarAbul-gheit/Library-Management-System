from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, RequestPasswordResetViewSet, ConfirmPasswordResetViewSet

router = DefaultRouter()
router.register(prefix='password-reset/request', viewset=RequestPasswordResetViewSet, basename='request-password-reset')
router.register(prefix='password-reset/confirm', viewset=ConfirmPasswordResetViewSet, basename='confirm-password-reset')

urlpatterns = [
    path(route='register/', view=RegisterView.as_view(), name='register'),
    path(route='login/', view=LoginView.as_view(), name='login'),
    path('', include(router.urls))
]