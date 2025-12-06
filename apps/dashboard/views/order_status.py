from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from apps.restaurants.models import Orders
from apps.dashboard.serializers import OrderStatusSerializer

class OrderStatusAPIView(ListAPIView):
    queryset = Orders.objects.prefetch_related("items", "table").order_by("-created_at")
    serializer_class = OrderStatusSerializer
    permission_classes = [IsAuthenticated]
