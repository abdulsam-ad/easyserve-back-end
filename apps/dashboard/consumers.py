# from channels.generic.websocket import AsyncJsonWebsocketConsumer
#
#
# class OrderStatusConsumer(AsyncJsonWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         await self.channel_layer.group_add("orders", self.channel_name)
#
#     async def disconnect(self, code):
#         await self.channel_layer.group_discard("orders", self.channel_name)
#
#     async def order_update(self, event):
#         message = event.get("message")
#         await self.send_json(message)
#
#     async def receive_json(self, content, **kwargs):
#         pass
