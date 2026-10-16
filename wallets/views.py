from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import response
from .serializers import WalletSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Wallet

# Create your views here.

class WalletDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet = Wallet.objects.get(user=request.user)
        serializer = WalletSerializer(wallet)

        return response(serializer.data)