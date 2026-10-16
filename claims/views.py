from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import process_claim

# Create your views here.
class ClaimPointsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        result = process_claim(request.user)

        if result['Success']:
            return Response(result, status=200)
        return Response(result, status=400)