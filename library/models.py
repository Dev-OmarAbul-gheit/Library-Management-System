from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Library(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255, unique=True)
    latitude = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Library"
        verbose_name_plural = "Libraries"


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
    cover_image = models.ImageField(upload_to='library/books/images')
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