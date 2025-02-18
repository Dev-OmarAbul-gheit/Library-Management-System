from django.utils.crypto import get_random_string


def generate_otp():
    return get_random_string(length=5, allowed_chars="0123456789")