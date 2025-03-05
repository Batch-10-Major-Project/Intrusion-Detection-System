import pyotp
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    two_factor_secret = models.CharField(max_length=100, blank=True, null=True)

    def generate_otp_secret(self):
        """Generate and save a new OTP secret for the user."""
        if not self.two_factor_secret:
            self.two_factor_secret = pyotp.random_base32()
            self.save()
