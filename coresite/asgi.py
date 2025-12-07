import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from apps.dashboard.middleware import TokenAuthMiddleware
from apps.dashboard.routing import websocket_urlpatterns


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coresite.settings')

app = get_asgi_application()


application = ProtocolTypeRouter({
    "http": app,
    "websocket": TokenAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    ),
})
