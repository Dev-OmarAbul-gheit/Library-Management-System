from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .models import Library
from .serializers import LibrarySerializer


class LibraryViewSet(ModelViewSet):
    queryset = Library.objects.prefetch_related('books__category', 'books__author').all()
    serializer_class = LibrarySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'books__category', 'books__author']