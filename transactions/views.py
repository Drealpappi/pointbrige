from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from .serializers import RedeemPointsSerializer
from .services import redeem_points

class RedeemPointsView(APIView):
    """
    API view to handle user reward points redemption.
    It Utilizes a service layer to process the transaction safety checks.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = RedeemPointsSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        points_to_redeem = serializer.validated_data['points']

        try:
            result = redeem_points(request.user, points_to_redeem)
            return Response({
                "success": True,
                "message": "Redemption successful!!",
                "data": result
            }, status=status.HTTP_200_OK)
            
        except ValidationError as e:
            error_message = e.message if hasattr(e, 'message') else str(e)
            if hasattr(e, 'message_dict'):
                error_message = e.message_dict
                
            return Response({
                "success": False,
                "error": error_message
            }, status=status.HTTP_400_BAD_REQUEST)