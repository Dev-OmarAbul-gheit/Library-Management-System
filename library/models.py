from django.db import models
from django.conf import settings
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.contrib.gis.db import models as gis_models


class Library(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255, unique=True)
    coordinates = gis_models.PointField(geography=True, srid=4326, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def clean_coordinates(self, coordinates):
        latitude = coordinates[0]
        longitude = coordinates[1]
        if latitude < -90 or latitude > 90:
            raise ValidationError("Latitude must be between -90 and 90")
        if longitude < -180 or longitude > 180:
            raise ValidationError("Longitude must be between -180 and 180")
        return coordinates
    
    class Meta:
        verbose_name = 'Library'
        verbose_name_plural = 'Libraries'


class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Book(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    publication_date = models.DateTimeField(null=True, blank=True)
    cover_image = models.ImageField(upload_to='library/books/images', null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    libraries = models.ManyToManyField(Library, through='LibraryBook', related_name='books')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'


class LibraryBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    is_borrowed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title} at {self.library.name}"


class BorrowingTransaction(models.Model):
    book = models.ForeignKey(LibraryBook, on_delete=models.CASCADE)
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    borrowing_price = models.DecimalField(max_digits=6, decimal_places=2)
    borrowing_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned_date = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.book.book.title} borrowed by {self.borrower.username}"
    
    @property
    def daily_penalty_value(self):
        # Assuming the daily penalty is 1% of the borrowing price
        return self.price * 0.01
    
    @property
    def is_borrowed(self) -> bool:
        return self.book.is_borrowed

    def calculate_penalty(self) -> float:
            if self.returned_date > self.due_date:
                days_late = (self.returned_date - self.due_date).days
                total_penalty = days_late * self.daily_penalty_value
            else:
                total_penalty = 0.00
            return total_penalty