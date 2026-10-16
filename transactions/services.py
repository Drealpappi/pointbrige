from decimal import Decimal, ROUND_DOWN
from django.db import transaction
from django.core.exceptions import ValidationError
from wallets.models import Wallet
from rewards.models import RewardPoint
from .models import RedemptionTransaction

CONVERSION_RATE = 1000
MINIMUM_REDEMPTION = 1000

@transaction.atomic
def redeem_points(user, points):
    if points < MINIMUM_REDEMPTION:
        raise ValidationError(
            f"Minimum redemption is 1000 points"
        )
    reward = None
    wallet = None
    try:
        reward = RewardPoint.objects.select_for_update().get(user=user)
    except RewardPoint.DoesNotExist:
        raise ValidationError("Wallet profile not found for this user.")
    try:
        wallet = Wallet.objects.select_for_update().get(user=user)
    except Wallet.DoesNotExist:
        raise ValidationError(
            "Wallet profile not found for this user."
        )


    if reward.points < points:
        raise ValidationError(
            f"Insufficient points. Available points: {reward.points}"
        )
    
    raw_amount = Decimal(points) / Decimal(CONVERSION_RATE)
    amount = raw_amount.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
    reward.points -= points
    reward.save()

    wallet.balance += amount
    wallet.save()

    RedemptionTransaction.objects.create(
        user=user,
        points_redeemed=points,
        amount_received=amount,
        conversion_rate=CONVERSION_RATE,
        status="success"
    )

    return {
        "points_redeemed": points,
        "amount_received": amount,
        "wallet_balance": wallet.balance
    }