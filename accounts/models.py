from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):

    id = models.BigAutoField(
        primary_key=True,)


    email = models.EmailField(
        unique=True,)

    phone_number = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,)

    username = models.CharField(
        max_length=30,
        unique=True,)

    is_client = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    referral_code = models.CharField(
        max_length=20,
        unique=True,
        null=True,
    blank=True,)

    referred_by = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="referrals",)

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = str(uuid.uuid4()).split("-")[0].upper()

        super().save(*args, **kwargs)