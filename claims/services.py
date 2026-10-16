from django.utils import timezone
from datetime import timedelta
from wallets.models import Wallet
from .models import ClaimHistory
from transactions.models import Transaction

POINT_PER_CLAIM = 50
CLAIM_COUNTDOWN_HOURS = 1
MAX_DAILY_CLAIMS = 5


def process_claim(user):
    wallet = Wallet.objects.get(
        User=user
    )
    now = timezone.now()

    last_claim = ClaimHistory.objects.filter(
        User=user
    ).order_by('created_at').first()

    if last_claim:
        cooldown_time = last_claim.created_at + timedelta(
            hours=CLAIM_COUNTDOWN_HOURS
        )

        if now < cooldown_time:
            remaining = cooldown_time - now
            return {
                "Success":False,
                "Message": f"cooldown active. Try aagin in {remaining}"
            }
        
    today_claims = ClaimHistory.objects.filter(
        User=user,
        created_at_date=now.date()
    ).count()

    if today_claims >= MAX_DAILY_CLAIMS:
        return {
            "Success": False,
            "Message": f"Daily claim limit reached"
        }
    
    wallet.points_balance += POINT_PER_CLAIM
    wallet.save()

    ClaimHistory.objects.create(
        User=user,
        points_claimed=POINT_PER_CLAIM
    )

    Transaction.objects.create(
        wallet=wallet,
        transaction_type='CLAIM',
        amount=POINT_PER_CLAIM,
        descriptio='Daily point claim'
    )

    return {
        "Success":True,
        "Message": f"{POINT_PER_CLAIM} Points claimed successfuly",
        "point_balance": wallet.points_balance
    }