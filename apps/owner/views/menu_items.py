from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from apps.restaurants.models import MenuItem
from apps.restaurants.serializers import MenuItemSerializer
from utils.notifications import create_notification
from utils.permissions import IsRestaurantOwner


class MenuItemViewSet(ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsRestaurantOwner()]

    def get_queryset(self):
        menu_id = self.request.query_params.get('menu_id')
        if menu_id:
            return MenuItem.objects.filter(menu_id=menu_id)
        return MenuItem.objects.none()

    def perform_create(self, serializer):
        instance = serializer.save()
        create_notification(
            profile=self.request.user.profile,
            message=f"New menu '{instance.name}' created for menu '{instance.menu.name}'."
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        create_notification(
            profile=self.request.user.profile,
            message=f"Menu Item '{instance.name}' updated for restaurant '{instance.menu.restaurant.name}'."
        )

    def perform_destroy(self, instance):
        menu_item_name = instance.name
        restaurant_name = instance.restaurant.name
        instance.delete()
        create_notification(
            profile=self.request.user.profile,
            message=f"Menu Item '{menu_item_name}' deleted from restaurant '{restaurant_name}'."
        )
