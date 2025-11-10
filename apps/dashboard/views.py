from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.dashboard.serializers import AssignedTableSerializer, CurrentOrderSerializer


class MyAssignedTablesView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def get(self, request):
        assigned_tables = request.user.profile.assigned_tables
        serializer = AssignedTableSerializer(assigned_tables, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CurrentOrdersView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def get(self, request):
        # Logic to retrieve current orders for the authenticated user
        current_orders = request.user.profile.waiter_orders
        serializer = CurrentOrderSerializer(current_orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)