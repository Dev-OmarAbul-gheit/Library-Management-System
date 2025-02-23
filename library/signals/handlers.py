from django.db.models.signals import m2m_changed, pre_delete
from django.dispatch import receiver
from library.models import BorrowingTransaction, ReturningTransaction


@receiver(m2m_changed, sender=BorrowingTransaction.books.through)
def mark_books_as_borrowed(sender, instance, action, **kwargs):
    if action == 'post_add':
        for book in instance.books.all():
            book.is_borrowed = True
            book.save()


@receiver(pre_delete, sender=BorrowingTransaction)
def mark_books_as_returned(sender, instance, **kwargs):
    for book in instance.books.all():
        book.is_borrowed = False
        book.save()


@receiver(m2m_changed, sender=ReturningTransaction.books.through)
def mark_books_as_returned(sender, instance, action, **kwargs):
    if action == 'post_add':
        for book in instance.books.all():
            book.is_borrowed = False
            book.save()