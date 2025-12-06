from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now

from apps.restaurants.models import Cart, Orders, OrderItem, MenuItem
from apps.restaurants.serializers import OrderDetailSerializer, OrderSerializer


class OrderCheckoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_profile = request.user.profile

        items = request.data.get("items")

        if not items or len(items) == 0:
            return Response({"detail": "Items are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        order_type = request.data.get("order_type", "DINE_IN")

        # Base order data
        order_data = {
            "user": user_profile,
            "ordered_date": now(),
            "order_type": order_type,
            "ordered": True,
            "payment_status": "Pending",
        }

        # Dine-in extra fields
        if order_type == "DINE_IN":
            order_data["table_id"] = request.data.get("table")
            order_data["waiter_id"] = request.data.get("waiter")

        # Online extra fields
        else:
            order_data.update({
                # "billing_first_name": request.data.get("billing_first_name"),
                "billing_first_name": request.user.profile.first_name,
                # "billing_last_name": request.data.get("billing_last_name"),
                "billing_last_name": request.user.profile.last_name,
                # "billing_email": request.data.get("billing_email"),
                "billing_email": request.user.email,
                # "billing_phone": request.data.get("billing_phone"),
                "billing_phone": request.user.profile.phone,
                "billing_address": request.data.get("billing_address", "123 Main St, City, Country"),
                # "billing_address": request.user.profile.address,
                "shipping_address": request.data.get("shipping_address", "123 Main St, City, Country"),
                # "shipping_address": request.user.profile.address,
            })

        # Create order
        order = Orders.objects.create(**order_data)

        total_price = 0

        # Add each item directly from frontend
        for item in items:
            menu_item_obj = get_object_or_404(MenuItem, id=item["menu_item"])

            order_item = OrderItem.objects.create(
                menu_item=menu_item_obj,
                quantity=item.get("quantity", 1),
                comments=item.get("comments", ""),
                price=menu_item_obj.price,
            )

            total_price += menu_item_obj.price * item.get("quantity", 1)

            order.items.add(order_item)

        # Set total price
        order.total_price = total_price
        order.save()

        return Response(OrderDetailSerializer(order).data, status=status.HTTP_201_CREATED)

class OrderCheckoutAPIViewOld(APIView):
    """
    Convert the current user's cart into an order.
    Supports both dine-in and online orders.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_profile = request.user.profile

        try:
            cart = Cart.objects.get(user=user_profile)
        except Cart.DoesNotExist:
            return Response({"detail": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

        if not cart.cart_items.exists():
            return Response({"detail": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        order_type = request.data.get("order_type", "DINE_IN")

        # Base order data
        order_data = {
            "user": user_profile,
            "ordered_date": now(),
            "order_type": order_type,
            "ordered": True,
            "payment_status": "Pending",
            "total_price": cart.total_price,
        }

        # Dine-in fields
        if order_type == "DINE_IN":
            order_data["table_id"] = request.data.get("table")
            order_data["waiter_id"] = request.data.get("waiter")

        # Online fields
        else:
            order_data["billing_first_name"] = request.data.get("billing_first_name")
            order_data["billing_last_name"] = request.data.get("billing_last_name")
            order_data["billing_email"] = request.data.get("billing_email")
            order_data["billing_phone"] = request.data.get("billing_phone")
            order_data["billing_address"] = request.data.get("billing_address")
            order_data["shipping_address"] = request.data.get("shipping_address")

        # Create order
        order = Orders.objects.create(**order_data)

        # Copy cart items → order items
        for cart_item in cart.cart_items.all():
            order_item = OrderItem.objects.create(
                menu_item=cart_item.menu_item,
                quantity=cart_item.quantity,
                comments=cart_item.comments,
                price=cart_item.price,
            )
            order.items.add(order_item)

        order.save()

        # Empty cart
        cart.cart_items.all().delete()
        cart.update_total_price()

        return Response(OrderDetailSerializer(order).data, status=status.HTTP_201_CREATED)

class WaiterOrderListAPIView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Orders.objects.filter(waiter=self.request.user.profile).order_by("-created_at")

class UserOrderHistoryAPIView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Orders.objects.filter(user=self.request.user.profile).order_by("-created_at")
