from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny,],

)


urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/user/', include('apps.core.urls')),
    path('api/restaurants/', include('apps.restaurants.urls')),
    path('api/user-profile/', include('apps.userprofile.urls')),
    path('api/api-auth/', include('rest_framework.urls')),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path("api/superadmin/", include("apps.super_admin.urls")),
    path("api/owner-menus/", include("apps.owner.urls.menus")),
    path("api/owner-category/", include("apps.owner.urls.category")),
    path("api/owner-menu-items/", include("apps.owner.urls.menu_items")),
    path("api/owner-menu-item-ingredients/", include("apps.owner.urls.menu_item_ingredients")),

    path('api/dashboard/', include('apps.dashboard.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
