from rest_framework import serializers

class RedeemSerializer(serializers.Serializer):
    points = serializers.IntegerField(min_value=1)