from rest_framework import serializers

class RedeemPointsSerializer(serializers.Serializer):
    reward_id = serializers.IntegerField(required=True)
    points_cost = serializers.IntegerField(required=True, min_value=1)
    reward_name = serializers.CharField(max_length=100, required=True)