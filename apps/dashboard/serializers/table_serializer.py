from rest_framework import serializers
from apps.restaurants.models import TABLE_STATE

class TableSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    number = serializers.IntegerField()
    status = serializers.ChoiceField(
        choices=[label for _, label in TABLE_STATE]
    )
    customers = serializers.IntegerField()
    orderItems = serializers.ListField()
    orderTime = serializers.DateTimeField(allow_null=True)
    orderId = serializers.IntegerField(allow_null=True)
    customer_name = serializers.CharField(allow_null=True)
    review = serializers.DictField(allow_null=True)
