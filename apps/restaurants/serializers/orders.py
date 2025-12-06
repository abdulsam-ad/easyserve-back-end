from rest_framework import serializers
from apps.restaurants.models import Orders, OrderItem, MenuItem


class MenuItemNameSerializer(serializers.ModelSerializer):
    """
    Serializer to get only the name of the MenuItem.
    """
    class Meta:
        model = MenuItem
        fields = ['name']

class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderItem model.
    """
    menu_item = MenuItemNameSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = "__all__"

class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Orders
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model.
    """
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Orders
        fields = "__all__"