from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from celery import shared_task
from .models import BorrowingTransaction

@shared_task
def send_borrowing_email_async(borrowing_data):
    subject = 'Borrowing Confirmation'
    html_message = render_to_string('emails/borrowing_email.html', borrowing_data)
    send_mail(
        subject=subject,
        message=html_message,
        from_email='library@example.com',
        recipient_list=[borrowing_data['email']],
        html_message=html_message,
    )

@shared_task
def notify_borrowers_async():
    queryset = BorrowingTransaction.objects.select_related('borrower').prefetch_related('books__book')
    transactions = [
        transaction for transaction in queryset 
        if transaction.due_date - timezone.now().date() <= timezone.timedelta(days=3) 
        and transaction.books.filter(is_borrowed=True).exists()
    ]

    for transaction in transactions:
        notify_email_data = {
            'username' : transaction.borrower.username,
            'books': [{
                'title': book.book.title,
                'author': book.book.author.name,
                'library': book.library.name
            } for book in transaction.books.filter(is_borrowed=True)],
            'due_date' : transaction.due_date
        }
        html_message = render_to_string('emails/borrowing_reminder_email.html', notify_email_data)
        send_mail(
            subject='Borrowing Due Date Reminder',
            message=html_message,
            from_email='admin@platform.com',
            recipient_list=[transaction.borrower.email],
            html_message=html_message,
        )

    