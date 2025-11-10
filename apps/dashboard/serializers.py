from rest_framework import serializers
from apps.restaurants.models import Table, Orders


class AssignedTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Table
        fields = [
            "id",
            "table_number",
            "table_state",
            "customer_count",
            "updated_at",
            "orders",
        ]

class CurrentOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = [
            "id",
            "table",
            "user",
            "items",
            "updated_at",
            "order_status",
        ]