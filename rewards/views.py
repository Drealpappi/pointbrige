from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rewards.services import add_points
from .redeem_service import redeem_points
from .serializers import RedeemSerializer
from datetime import date
from rewards.models import RewardPoint

# Create your views here.
class ClaimDailyRewardView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        reward_account = RewardPoint.object.get(
            user=request.user
        )

        today = date.todat()

        if reward_account.last_claim_date == today:
            return Response(
                {
                    "error":
                    "You have already claimed today's reward. Try again tomorrow"
                }
            )
        
        add_points(
            user=request.user,
            points=500,
            description="Daily login bonus"
        )

        reward_account.last_claim_date = today
        reward_account.save()

class RedeemPointsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RedeemSerializer(data=request.data)

        if serializer.is_valid():
            try:
                balance = redeem_points(
                    request.user,
                    serializer.validated_data["points"]
                )

                return Response({
                    "message": "Points redeemed successfully",
                    "wallet_balance": balance
                })
            except ValueError as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )