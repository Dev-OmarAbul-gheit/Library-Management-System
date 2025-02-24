from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models as gis_models
from .mixins import OTPMixin
from .utils import generate_otp, set_otp_expire_date



class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    coordinates = gis_models.PointField(geography=True, srid=4326, null=True, blank=True)

    def __str__(self) -> str:
        return self.username


class PasswordResetOTP(OTPMixin, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=5, unique=True, default=generate_otp)
    expires_at = models.DateTimeField(default=set_otp_expire_date)

    def __str__(self):
        return self.otp