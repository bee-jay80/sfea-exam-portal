import secrets
from datetime import timedelta

from django.contrib.auth.hashers import make_password
from django.utils import timezone

from accounts.models import OTP

def generate_otp(user, purpose):
    # Generate a secure 6-digit OTP
    otp = f"{secrets.randbelow(1_000_000):06d}"

    # Hash the OTP before storing it
    otp_hash = make_password(otp)

    # Set expiration time
    expires_at = timezone.now() + timedelta(minutes=5)

    # Create or update the user's OTP record
    OTP.objects.update_or_create(
        user=user,
        defaults={
            "otp_hash": otp_hash,
            "purpose": purpose,
            "expires_at": expires_at,
            "attempts": 0,
            "is_used": False,
        }
    )

    # Return the plain OTP for email delivery
    return otp



from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.utils import timezone

from accounts.models import OTP

User = get_user_model()

def verify_otp(email, submitted_otp, purpose):
    try:
        user = User.objects.get(email__iexact=email)
        otp_record = OTP.objects.get(user=user)

    except (User.DoesNotExist, OTP.DoesNotExist):
        return False, "Invalid OTP or email."

    # Check purpose
    if otp_record.purpose != purpose:
        return False, "Invalid OTP or email."

    # Check whether OTP has already been used
    if otp_record.is_used:
        return False, "This OTP has already been used."

    # Check expiration
    if timezone.now() > otp_record.expires_at:
        return False, "OTP has expired. Request a new one."

    # Limit verification attempts
    if otp_record.attempts >= 5:
        return False, "Too many attempts. Request a new OTP."

    # Verify submitted OTP against stored hash
    if not check_password(submitted_otp, otp_record.otp_hash):
        otp_record.attempts += 1
        otp_record.save(update_fields=["attempts"])
        return False, "Invalid OTP."

    # Mark OTP as used
    otp_record.is_used = True
    otp_record.save(update_fields=["is_used"])

    return True, user