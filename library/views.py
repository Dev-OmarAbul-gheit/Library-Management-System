from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Library, Author, Book, BorrowingTransaction
from .serializers import (LibrarySerializer, AuthorSerializer,
                          BookSerializer, CreateBorrowingTransactionSerializer,
                          BorrowingTransactionSerializer)


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
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'borrow_book':
            return CreateBorrowingTransactionSerializer            
        return BorrowingTransactionSerializer

    @action(detail=False, methods=['post'], url_path='borrow', url_name='borrow-book', permission_classes=[IsAuthenticated])
    def borrow_book(self, request):
        serializer = self.get_serializer(data=request.data, context = {'borrower': request.user})
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save()
        serializer = BorrowingTransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'], url_path='history', url_name='transactions-history', permission_classes=[IsAuthenticated])
    def view_history(self, request):
        queryset = self.get_queryset().filter(borrower=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)