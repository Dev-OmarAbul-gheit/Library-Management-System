from django.contrib import admin
from .models import Library, Author, Category, Book, LibraryBook, BorrowingTransaction


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    pass


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass


@admin.register(LibraryBook)
class LibraryBookAdmin(admin.ModelAdmin):
    pass


@admin.register(BorrowingTransaction)
class BorrowingTransactionAdmin(admin.ModelAdmin):
    pass
