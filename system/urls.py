from django.urls import path
from .views import RegisterView, LoginView

urlpatterns = [
    path(route='register/', view=RegisterView.as_view(), name='register'),
    path(route='login/', view=LoginView.as_view(), name='login')

] 