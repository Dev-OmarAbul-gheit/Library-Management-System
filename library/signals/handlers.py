from django.db.models.signals import m2m_changed, pre_delete, post_save
from django.dispatch import receiver
from library.models import BorrowingTransaction, ReturningTransaction
from library.tasks import send_borrowing_email_async


@receiver(m2m_changed, sender=BorrowingTransaction.books.through)
def mark_books_as_borrowed(sender, instance, action, **kwargs):
    if action == "post_add":
        for book in instance.books.all():
            book.is_borrowed = True
            book.save()


@receiver(m2m_changed, sender=BorrowingTransaction.books.through)
def send_borrowing_email(sender, instance, action, **kwargs):
    if action == "post_add":
        books = instance.books.select_related("book__author", "library").all()
        borrowing_data = {
            "username": instance.borrower.username,
            "email": instance.borrower.email,
            "books": [
                {
                    "title": book.book.title,
                    "author": book.book.author.name,
                    "library": book.library.name,
                }
                for book in books
            ],
            "borrowing_date": instance.borrowing_date,
            "due_date": instance.due_date,
        }
        send_borrowing_email_async.delay(borrowing_data)


@receiver(pre_delete, sender=BorrowingTransaction)
def delete_borrowing(sender, instance, **kwargs):
    for book in instance.books.all():
        book.is_borrowed = False
        book.save()


@receiver(m2m_changed, sender=ReturningTransaction.books.through)
def mark_books_as_returned(sender, instance, action, **kwargs):
    if action == "post_add":
        for book in instance.books.all():
            book.is_borrowed = False
            book.save()
