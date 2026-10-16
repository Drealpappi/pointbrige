from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from wallets.models import Wallet
from django.conf import settings

# Create your models here.
class Transaction(models.Model):
    
    TRANSACTION_TYPES = (
        ('CLAIM', 'Claim'),
        ('REDEEM', 'Redeem'),
        ('FUND', 'Fund'),
        ('WITHDRAW', 'Withdraw'),
    )

    wallet = models.ForeignKey(
        'wallets.Wallet',
        on_delete=models.CASCADE,
        related_name='transactions'
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES
    )

    amount = models.DecimalField( 
        decimal_places=2,
        max_digits=12
    )

    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.wallet.user.username} - {self.transaction_type}"
    
class RedemptionTransaction(models.Model):

    STATUS_CHOICES = (
        ("success", "success"),
        ("failed", "failed"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    points_redeemed = models.PositiveBigIntegerField()
    amount_received = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    conversion_rate = models.PositiveBigIntegerField(
        default=1000
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="success"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} redeemed {self.points_redeemed}"