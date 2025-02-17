from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, RequestPasswordResetViewSet

router = DefaultRouter()
router.register(prefix='password-reset/request', viewset=RequestPasswordResetViewSet, basename='request-password-reset')

urlpatterns = [
    path(route='register/', view=RegisterView.as_view(), name='register'),
    path(route='login/', view=LoginView.as_view(), name='login'),
    path('', include(router.urls))
]