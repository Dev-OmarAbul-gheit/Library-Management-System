from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Library, Author, Book, BorrowingTransaction
from .serializers import LibrarySerializer, AuthorSerializer, BookSerializer, BorrowingTransactionSerializer


class LibraryViewSet(ReadOnlyModelViewSet):
    queryset = Library.objects.prefetch_related('books__category', 'books__author').distinct().all()
    serializer_class = LibrarySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'books__category', 'books__author']


class AuthorViewSet(ReadOnlyModelViewSet):
    queryset = Author.objects \
                     .annotate(book_count=Count('books')) \
                     .prefetch_related('books__category', 'books__libraries') \
                     .all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['books__category', 'books__libraries']


class BookViewSet(ReadOnlyModelViewSet):
    queryset = Book.objects \
                   .select_related('category', 'author') \
                   .prefetch_related('libraries') \
                   .all()
    serializer_class = BookSerializer


class BorrowingTransactionViewSet(ReadOnlyModelViewSet):
    queryset = BorrowingTransaction.objects.all()
    serializer_class = BorrowingTransactionSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='borrow', url_name='borrow-book')
    def borrow_book(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)