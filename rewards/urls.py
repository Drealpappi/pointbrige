from django.urls import path, include
from .views import ClaimDailyRewardView, RedeemPointsView

urlpatterns = [
    path("claimdaily/", ClaimDailyRewardView.as_view(), name="claim-daily"),
    path("redeem/", RedeemPointsView.as_view(), name="redeem-points"),
]