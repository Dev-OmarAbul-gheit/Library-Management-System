from rest_framework.viewsets import ModelViewSet
from .models import Library
from .serializers import LibrarySerializer


class LibraryViewSet(ModelViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer