from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperAdmin(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.user_type == "super_admin"
        )

class IsSuperAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return (
            request.user.is_authenticated
            and request.user.user_type == "super_admin"
        )


class IsSuperAdminOrRestaurantOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if [IsRestaurantOwner().has_object_permission(request, view, obj)]:
            return True
        return False

    def has_permission(self, request, view):
        return request.user.is_authenticated

class IsRestaurantOwnerOld(BasePermission):

    def has_permission(self, request, view):
        # Must be authenticated and have user_type='restaurant_owner'
        user = request.user
        return user.is_authenticated and getattr(user, "user_type", None) == "restaurant_owner"

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "restaurant"):
            return obj.restaurant.owners.filter(id=request.user.id).exists()
        return False

class IsRestaurantOwner(BasePermission):
    def has_permission(self, request, view):
        # Must be authenticated and have user_type='restaurant_owner'
        user = request.user
        return user.is_authenticated and getattr(user, "user_type", None) == "restaurant_owner"

    def has_object_permission(self, request, view, obj):
        user = request.user

        restaurant = self._find_restaurant(obj)

        return restaurant and restaurant.owners.filter(id=user.id).exists()

    def _find_restaurant(self, obj, visited=None):
        """
        Recursively climbs through ForeignKey relationships
        until a Restaurant object or restaurant field is found.
        """
        if visited is None:
            visited = set()

        # Avoid infinite loops (in case of circular relations)
        if id(obj) in visited:
            return None
        visited.add(id(obj))

        # 1. If the object itself is a Restaurant
        if obj.__class__.__name__.lower() == "restaurant":
            return obj

        # 2. If the object directly has a 'restaurant' field
        if hasattr(obj, "restaurant"):
            return getattr(obj, "restaurant")

        # 3. Search through all foreign key–like attributes
        for field in obj._meta.get_fields():
            # Only traverse relations (ForeignKey, OneToOne)
            if field.is_relation and hasattr(obj, field.name):
                related_obj = getattr(obj, field.name, None)
                if related_obj is not None:
                    restaurant = self._find_restaurant(related_obj, visited)
                    if restaurant:
                        return restaurant

        return None
