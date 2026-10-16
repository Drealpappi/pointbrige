from decimal import Decimal
from django.db import transaction
from rewards.models import RewardPoint, RewardTransaction
from wallets.models import Wallet

CONVERSION_RATE = 1000 # 1000 points = $1

@transaction.atomic
def redeem_points(user, points):
    reward_account = RewardPoint.objects.select_for_update().get(user=user)
    wallet = Wallet.objects.select_for_update().get(user=user)

    if reward_account.points < points:
        raise ValueError("Insufficient reward points")

    cash = Decimal(points) / Decimal(CONVERSION_RATE)
    reward_account.points -= points
    reward_account.save()

    wallet.balance += cash
    wallet.save()

    RewardTransaction.objects.create(
        user=user,
        transaction_type="redeem",
        points=points,
        description=f"Redeemed {points} points successfully"

    )

    return wallet.balance