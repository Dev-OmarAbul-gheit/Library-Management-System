from django.core.mail import send_mail
from django.template.loader import render_to_string
from django_lifecycle import AFTER_CREATE, LifecycleModelMixin, hook


class OTPMixin(LifecycleModelMixin):
    @hook(AFTER_CREATE)
    def send_email_with_otp(self):
        data = {
            'username': self.user.username,
            'otp': self.otp,
            'reset_link' : f'http://127.0.0.1:8000/users/password-reset/confirm/'
        }
        body = render_to_string('emails/password-reset-email.html', data)
        send_mail(
            subject='Password Reset Request',
            message=body,
            html_message=body,
            from_email='admin@platform.com',
            recipient_list=[self.user.email]
        )