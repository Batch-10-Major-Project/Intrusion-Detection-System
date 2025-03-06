from django.contrib.auth.models import AbstractUser
from django.db import models
import pyotp

class CustomUser(AbstractUser):
    two_factor_secret = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        app_label = 'ids' 

    def generate_otp_secret(self):
        """Generate and save a new OTP secret for the user."""
        if not self.two_factor_secret:
            self.two_factor_secret = pyotp.random_base32()
            self.save()

