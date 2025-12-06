# class TokenAuthMiddleware:
#     def __init__(self, inner):
#         self.inner = inner
#
#     async def __call__(self, scope, receive, send):
#         from django.contrib.auth.models import AnonymousUser
#         from rest_framework_simplejwt.tokens import AccessToken
#         from asgiref.sync import sync_to_async
#         from urllib.parse import parse_qs
#
#         query_params = parse_qs(scope.get("query_string", b"").decode())
#         token = query_params.get("token", [None])[0]
#
#         if token:
#             try:
#                 validated = AccessToken(token)
#                 user_id = validated["user_id"]
#                 from django.contrib.auth import get_user_model
#                 user = await sync_to_async(get_user_model().objects.get)(id=user_id)
#                 scope["user"] = user
#             except Exception as exc:
#                 print(exc)
#                 scope["user"] = AnonymousUser()
#         else:
#             scope["user"] = AnonymousUser()
#
#         return await self.inner(scope, receive, send)
