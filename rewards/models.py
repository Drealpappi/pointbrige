from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class RewardPoint(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reward_account"
    )

    points = models.PositiveBigIntegerField(default=0)
    last_claim = models.DateField(
        null=True,
        blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.points} points"
    
class RewardTransaction(models.Model):

    TRANSACTION_TYPES = (
        ("earn", "Earn"),
        ("redeem", "Redeem"),
        ("points", "Points"),
        ("penalty", "Penalty")
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reward_transactions"
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES
    )

    points = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{"self.user.username"}",
            f"{"self.transactio_type"}",
            f"{"self.points"}"
        )