from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.dashboard.services import TableService
from apps.dashboard.serializers import TableSerializer


class TablesListView(APIView):

    def get(self, request):
        service = TableService()
        tables_data = service.get_tables_data(self)

        serializer = TableSerializer(tables_data, many=True)
        return Response({"tables": serializer.data}, status=status.HTTP_200_OK)
