import uuid

from django.conf import settings
from django.db import models
from apps.common.models import BaseModel

class OTP(models.Model, BaseModel):

    class Purpose(models.TextChoices):
        EMAIL_VERIFICATION = "email_verification", "Email Verification"
        PASSWORD_RESET = "password_reset", "Password Reset"


    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="otps",
    )

    otp_hash = models.CharField(max_length=255)

    purpose = models.CharField(
        max_length=30,
        choices=Purpose.choices,
    )

    expires_at = models.DateTimeField()

    attempts = models.PositiveSmallIntegerField(default=0)

    is_used = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["user", "purpose"]),
        ]

    def __str__(self):
        return f"OTP for {self.user.email} - Purpose: {self.purpose}"