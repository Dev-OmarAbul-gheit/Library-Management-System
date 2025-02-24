from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Library, Author, Book, BorrowingTransaction, ReturningTransaction
from .serializers import (LibrarySerializer, AuthorSerializer, LoadedAuthorSerializer,
                          BookSerializer, CreateBorrowingTransactionSerializer,
                          BorrowingTransactionSerializer, ReturningTransactionSerializer)


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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['books__category', 'books__libraries']

    def get_serializer_class(self):
        if self.action == 'loaded':
            return LoadedAuthorSerializer
        return AuthorSerializer

    @action(detail=False, methods=['GET'], url_path='loaded', url_name='loaded-authors')
    def loaded(self, request):
        queryset = Author.objects.prefetch_related('books__category').all()
        for backend in self.filter_backends:
            queryset = backend().filter_queryset(self.request, queryset, self)        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookViewSet(ReadOnlyModelViewSet):
    queryset = Book.objects \
                   .select_related('category', 'author') \
                   .prefetch_related('libraries') \
                   .all()
    serializer_class = BookSerializer


class TransactionsViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        if self.action == 'borrow_book':
            return BorrowingTransaction.objects.all()
        return ReturningTransaction.objects.all()

    def get_serializer_class(self):
        if self.action == 'borrow_book':
            return CreateBorrowingTransactionSerializer
        elif self.action == 'return_book':
            return ReturningTransactionSerializer
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
        borrowing_queryset = BorrowingTransaction.objects.filter(borrower=request.user)
        borrowing_serializer = BorrowingTransactionSerializer(borrowing_queryset, many=True)

        returning_queryset = ReturningTransaction.objects.filter(borrower=request.user)
        returning_serializer = ReturningTransactionSerializer(returning_queryset, many=True)

        data = {
            'borrowing_transactions': borrowing_serializer.data,
            'returning_transactions': returning_serializer.data
        }
        return Response(data)
    
    @action(detail=False, methods=['post'], url_path='return', url_name='return-book', permission_classes=[IsAuthenticated])
    def return_book(self, request):
        serializer = self.get_serializer(data=request.data, context = {'borrower': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)