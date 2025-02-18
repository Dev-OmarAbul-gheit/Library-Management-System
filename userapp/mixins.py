from django.utils import timezone
from django_lifecycle import BEFORE_CREATE, LifecycleModelMixin, hook


class OTPMixin(LifecycleModelMixin):
    @hook(BEFORE_CREATE)
    def set_expire_at(self):
        self.expires_at = timezone.now() + timezone.timedelta(minutes=10)
