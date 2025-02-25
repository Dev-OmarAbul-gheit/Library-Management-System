from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string


@shared_task
def send_email_with_otp__async(data):
    body = render_to_string("emails/password-reset-email.html", data)
    send_mail(
        subject="Password Reset Request",
        message=body,
        html_message=body,
        from_email="admin@platform.com",
        recipient_list=[data["email"]],
    )
