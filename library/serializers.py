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
    class Meta:
        model = BorrowingTransaction
        fields = ['id', 'books', 'borrower', 'borrowing_price', 'borrowing_date', 'due_date']


class CreateBorrowingTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = BorrowingTransaction
        fields = ['id', 'books', 'due_date']

    def validate(self, validated_data):
    
        # check the number of books being borrowed by the user
        borrower = self.context['borrower']
        total_borrowed_books = sum(transaction.books.count() for transaction in BorrowingTransaction.objects.filter(borrower=borrower))
        if total_borrowed_books >= 3:
            raise serializers.ValidationError('The user has already borrowed 3 books, can not borrow more books.')
        
        # validate the number of books at current borrowing transaction
        books = validated_data['books']
        if total_borrowed_books+ len(books) > 3:
            raise serializers.ValidationError(f'You cannot borrow {len(books)} more books as you already borrowed {total_borrowed_books} and you can not borrow more than 3 books.')

        # validate each book individually to ensure it is not being borrowed
        for book in books:
            if book.is_borrowed:
                raise serializers.ValidationError(f'The book "{book.book.title}" is currently being borrowed, choose another book or try again later.')

        # validate the due date
        due_date = validated_data['due_date']
        borrowing_date = timezone.now().date()
        max_period_month = 1
        max_return_date = borrowing_date + timedelta(days=max_period_month * 30)
        if due_date > max_return_date:
            raise serializers.ValidationError(f'Return date cannot be more than {max_period_month} month(s) from today.')

        return validated_data
    
    def create(self, validated_data):

        book_prices = sum([book.book.price for book in validated_data['books']])
        # assume the borrowing price is 25% of the books price
        borrowing_price = book_prices * Decimal(0.25)
        validated_data['borrowing_price'] = borrowing_price

        borrower = self.context['borrower']
        validated_data['borrower'] = borrower
        
        # create the borrowing transaction
        borrowing_transaction = super().create(validated_data)

        # set the books as borrowed
        for book in borrowing_transaction.books.all():
            book.is_borrowed = True
            book.save()

        return borrowing_transaction