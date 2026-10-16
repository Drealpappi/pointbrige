from django.db import transaction
from .models import RewardPoint, RewardTransaction
from django.core.exceptions import ValidationError

@transaction.atomic
def add_points(user, points, description=''):
    reward_account = RewardPoint.objects.select_for_update().get(
        user=user
    )

    reward_account.points += points
    reward_account.save()

    RewardTransaction.objects.create(
        user=user,
        transaction_type="EARNED",
        points=points,
        desciption=description
    )

    return reward_account

@transaction.atomic
def deduct_points(user, points, description=''):
    reward_account = RewardPoint.objects.select_for_update().get(
        user=user
    )

    if reward_account.points < points:
        raise ValidationError(
            "Insufficient reward points"
        )
    reward_account.points -= points
    reward_account.save()

    RewardTransaction.objects.create(
        user=user,
        transaction_type="redeem",
        points=points,
        description=description
    )
    return reward_account