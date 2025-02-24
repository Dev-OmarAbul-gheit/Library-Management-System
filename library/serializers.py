from datetime import timedelta
from decimal import Decimal
from django.utils import timezone
from rest_framework import serializers
from .models import Library, Author, Book, Category, LibraryBook, BorrowingTransaction, ReturningTransaction


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
        total_borrowed_books = sum([transaction.books.filter(is_borrowed=True).count() for transaction in BorrowingTransaction.objects.filter(borrower=borrower)])
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
        elif due_date < timezone.now().date():
            raise serializers.ValidationError('Return date cannot be in the past.')

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

        return borrowing_transaction
    

class ReturningTransactionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ReturningTransaction
        fields = ['id', 'books', 'borrower', 'return_date', 'late_return_penalty']
        extra_kwargs = {
            'borrower': {'read_only': True},
            'returning_date': {'read_only': True},
            'late_return_penalty': {'read_only': True}
        }

    def get_borrower_books(self, borrower):
        borrower_books = {
            book: transaction.due_date for transaction in BorrowingTransaction.objects.filter(borrower=borrower) for book in transaction.books.all() if book.is_borrowed
        }
        return borrower_books
    
    def get_book_penalty(self, book, due_date):
        today = timezone.now().date()
        late_days = (today - due_date).days
        penalty = 0.0
        if late_days > 0:
            penalty = book.book.price * Decimal(0.05) * late_days
        return penalty

    def validate_books(self, returned_books):
        borrower = self.context['borrower']
        borrower_books = self.get_borrower_books(borrower)
        for book in returned_books:
            if book not in borrower_books:
                raise serializers.ValidationError(f'The book "{book.book.title}" is not being borrowed by the user.')     
        return returned_books
    
    def create(self, validated_data):
        borrower = self.context['borrower']
        validated_data['borrower'] = borrower

        # handle late return penalty for each book, assume daily penalty is 5% of the book price
        books = validated_data['books']
        borrower_books = self.get_borrower_books(borrower)
        total_penalty = sum([self.get_book_penalty(book, borrower_books[book]) for book in books])
        validated_data['late_return_penalty'] = total_penalty

        return super().create(validated_data)
    

class SimpleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class SimpleBookSerializer(serializers.ModelSerializer):
    category = SimpleCategorySerializer()
    class Meta:
        model = Book
        fields = ['id', 'title', 'summary', 'category']


class LoadedAuthorSerializer(serializers.ModelSerializer):
    books = SimpleBookSerializer(many=True)
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'books']
