from django.utils import timezone
from django.utils.crypto import get_random_string


def generate_otp():
    return get_random_string(length=5, allowed_chars="0123456789")


def set_otp_expire_date():
    return timezone.now() + timezone.timedelta(minutes=10)
