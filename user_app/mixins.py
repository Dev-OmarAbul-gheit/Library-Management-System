from django.core.mail import send_mail
from django.template.loader import render_to_string
from django_lifecycle import AFTER_CREATE, LifecycleModelMixin, hook
from .tasks import send_email_with_otp__async


class OTPMixin(LifecycleModelMixin):
    @hook(AFTER_CREATE)
    def send_email_with_otp(self):
        data = {
            'username': self.user.username,
            'email' : self.user.email,
            'otp': self.otp,
            'reset_link' : f'http://127.0.0.1:8000/users/password-reset/confirm/'
        }
        send_email_with_otp__async.delay(data)