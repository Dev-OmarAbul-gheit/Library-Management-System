from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .models import Library, Author, Book
from .serializers import LibrarySerializer, AuthorSerializer, BookSerializer


class LibraryViewSet(ModelViewSet):
    queryset = Library.objects.prefetch_related('books__category', 'books__author').distinct().all()
    serializer_class = LibrarySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'books__category', 'books__author']


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects \
                     .annotate(book_count=Count('books')) \
                     .prefetch_related('books__category', 'books__libraries') \
                     .all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['books__category', 'books__libraries']


class BookViewSet(ModelViewSet):
    queryset = Book.objects \
                   .select_related('category', 'author') \
                   .prefetch_related('libraries') \
                   .all()
    serializer_class = BookSerializer