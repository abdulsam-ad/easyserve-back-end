from rest_framework import serializers
from apps.restaurants.models import ORDER_STATUS


class OrderStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=[label for _, label in ORDER_STATUS]
    )
