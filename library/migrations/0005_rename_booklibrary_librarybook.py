# Generated by Django 5.1.4 on 2025-02-18 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0004_book_booklibrary_book_libraries"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="BookLibrary",
            new_name="LibraryBook",
        ),
    ]
