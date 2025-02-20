from rest_framework import serializers
from .models import Library, Author, Book


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