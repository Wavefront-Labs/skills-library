---
id: computing-software.web-development.django.django-channels-and-websockets
name: django-channels-and-websockets
category: computing-software
field: web-development
product: django
tags: [django-channels, websockets, asgi, channel-layers, django]
level: advanced
status: docs-checked
description: "Adding WebSockets to Django with Channels: ASGI routing, consumers, authentication, Redis channel layers and groups, sending from views and tasks, deployment and scaling."
sources:
  - https://channels.readthedocs.io/en/latest/
  - https://channels.readthedocs.io/en/latest/topics/channel_layers.html
  - https://channels.readthedocs.io/en/latest/deploying.html
  - https://channels.readthedocs.io/en/latest/topics/security.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Django Channels and WebSockets

## 1. Setup
```python
# asgi.py
import os
from django.core.asgi import get_asgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django_asgi = get_asgi_application()                       # initialise Django before importing consumers
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from chat.routing import websocket_urlpatterns
application = ProtocolTypeRouter({
    "http": django_asgi,
    "websocket": AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter(websocket_urlpatterns))),
})
# settings
INSTALLED_APPS = ["daphne", *INSTALLED_APPS, "channels"]   # daphne first: runserver becomes ASGI
ASGI_APPLICATION = "config.asgi.application"
CHANNEL_LAYERS = {"default": {"BACKEND": "channels_redis.core.RedisChannelLayer", "CONFIG": {"hosts": [env("REDIS_URL")]}}}
```
`AllowedHostsOriginValidator` checks the WebSocket `Origin` header against `ALLOWED_HOSTS`, so cross-origin pages cannot open authenticated sockets.

## 2. Consumer
```python
class RoomConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        self.room = self.scope["url_route"]["kwargs"]["room"]
        if not user.is_authenticated or not await can_join(user, self.room):
            await self.close(code=4403); return
        self.group = f"room_{self.room}"
        await self.channel_layer.group_add(self.group, self.channel_name)
        await self.accept()
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group, self.channel_name)
    async def receive_json(self, content):
        msg = await save_message(self.scope["user"], self.room, content["text"][:2000])
        await self.channel_layer.group_send(self.group, {"type": "chat.message", "id": msg.id, "text": msg.text})
    async def chat_message(self, event):                   # "chat.message" -> chat_message
        await self.send_json({"id": event["id"], "text": event["text"]})
```
ORM calls in async consumers go through `database_sync_to_async` (or async ORM methods like `aget`, `acreate`).

## 3. Sending from views or Celery tasks
```python
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
async_to_sync(get_channel_layer().group_send)(f"room_{room}", {"type": "chat.message", "id": m.id, "text": m.text})
```

## 4. Deployment
- Run with Daphne (`daphne -p 8001 config.asgi:application`) or another ASGI server such as Uvicorn (the Channels deployment docs link the ASGI server list); a proxy in front must support WebSocket upgrades.
- `channels_redis` is the only Django-maintained channel layer supported for production; the in-memory layer is for testing and local development.
- Client reconnect with backoff and resubscribe; messages sent while disconnected are lost unless you persist and replay.
- For one-way updates, SSE or HTMX polling may be simpler than Channels.

## 5. Testing
`channels.testing.WebsocketCommunicator` with pytest-asyncio to connect, send and assert messages.

## Verify
- [ ] Unauthenticated and cross-origin connections rejected; messages fan out across two app instances via Redis; reconnect works after a deploy.

## Checked
Date: 2026-10-25. Documentation: Channels docs source (django/channels main: installation, deploying, topics/authentication, security, channel_layers, consumers, databases, testing).
Confirmed: `daphne` first in `INSTALLED_APPS`, optional `"channels"` for `runworker`, `ProtocolTypeRouter`, `AuthMiddlewareStack`, `AllowedHostsOriginValidator`, `AsyncJsonWebsocketConsumer`, `database_sync_to_async` and async ORM methods, `channels_redis.core.RedisChannelLayer` config, `async_to_sync(channel_layer.group_send)`, `type` to handler-name mapping, `WebsocketCommunicator` with pytest-asyncio.
Corrected or removed: nginx `proxy_read_timeout` and header-forwarding specifics, and the "multiple instances require Redis" wording (replaced with the documented production-support statement).
Method: documentation only; no commands were run.
