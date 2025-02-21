from datetime import timedelta
from decimal import Decimal
from django.utils import timezone
from rest_framework import serializers
from .models import Library, Author, Book, LibraryBook, BorrowingTransaction


class LibrarySerializer(serializers.ModelSerializer):
    coordinates = serializers.ListField(child=serializers.FloatField())

    class Meta:
        model = Library
        fields = ['id', 'name', 'location', 'coordinates']


class AuthorSerializer(serializers.ModelSerializer):
    book_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'book_count']


class BookSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    class Meta:
        model = Book
        fields = ['id', 'title', 'summary', 'price', 'cover_image', 'author', 'category', 'libraries']


class BorrowingTransactionSerializer(serializers.ModelSerializer):
    borrowing_price = serializers.DecimalField(read_only=True, max_digits=6, decimal_places=2)
    class Meta:
        model = BorrowingTransaction
        fields = ['id', 'book', 'borrower', 'borrowing_price', 'borrowing_date', 'due_date']

    def validate_book(self, book):
        """
            Check if the book is already borrowed.
        """
        if book.is_borrowed:
            raise serializers.ValidationError('The book is already borrowed')
        return book
    
    def validate_due_date(self, due_date):
        borrowing_date = timezone.now().date()
        max_period_month = 1
        max_return_date = borrowing_date + timedelta(days=max_period_month * 30)
        if due_date > max_return_date:
            raise serializers.ValidationError(f'Return date cannot be more than {max_period_month} month(s) from today.')
        return due_date

    def validate_borrower(self, borrower):
        if BorrowingTransaction.objects.filter(borrower=borrower).count() >= 3:
            raise serializers.ValidationError('The borrower has already reached the maximum number of books allowed to be borrowed (3).')
        return borrower

    def create(self, validated_data):
        book_price = validated_data['book'].book.price
        borrowing_price = book_price * Decimal(0.1) # assume the borrowing price is 10% of the book price
        validated_data['borrowing_price'] = borrowing_price

        borrowing_transaction = super().create(validated_data)

        # set the book as borrowed
        borrowing_transaction.book.is_borrowed = True

        borrowing_transaction.book.save()
        return borrowing_transaction