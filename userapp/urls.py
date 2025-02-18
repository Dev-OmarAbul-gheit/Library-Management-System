from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RequestPasswordResetViewSet,UserViewSet

router = DefaultRouter()
router.register(prefix='users', viewset=UserViewSet, basename='users')
router.register(prefix='password-reset/request', viewset=RequestPasswordResetViewSet, basename='request-password-reset')

urlpatterns = [
    path('', include(router.urls))
]