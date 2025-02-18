from django.contrib import admin
from .models import Library, Author

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    pass


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass