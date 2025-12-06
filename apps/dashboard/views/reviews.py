from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apps.restaurants.serializers import ReviewCreateSerializer
from rest_framework.generics import ListAPIView
from apps.restaurants.models import Review
from apps.dashboard.serializers import ReviewListSerializer


class AddReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReviewCreateSerializer(data=request.data, context={"request": request})

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "Review submitted successfully"}, status=201)

class ReviewListAPIView(ListAPIView):
    queryset = Review.objects.select_related("order__table").order_by("-created_at")
    serializer_class = ReviewListSerializer
    permission_classes = [IsAuthenticated]
