from django.urls import path
from .views import RedeemPointsView

urlpatterns = [
    path("redeem/", RedeemPointsView.as_view(), name="redeem-points"),
]