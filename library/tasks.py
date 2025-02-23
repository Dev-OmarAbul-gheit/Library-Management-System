from django.core.mail import send_mail
from django.template.loader import render_to_string
from celery import shared_task

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