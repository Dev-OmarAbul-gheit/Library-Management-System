from djoser.serializers import UserCreateSerializer
from .models import User

class RegisterUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['id', 'username', 'email', 'password']