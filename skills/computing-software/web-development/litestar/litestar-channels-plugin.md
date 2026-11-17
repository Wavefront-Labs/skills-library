---
id: computing-software.web-development.litestar.litestar-channels-plugin
name: litestar-channels-plugin
category: computing-software
field: web-development
product: litestar
tags: [litestar, channels, pubsub, channelsplugin, websocket, backpressure, history, redis]
level: practitioner
status: docs-checked
description: "Use Litestar ChannelsPlugin to publish and subscribe to channels, replay history, bound subscriber backlogs, pick a backend, and generate websocket handlers."
sources: [https://docs.litestar.dev/latest/usage/channels.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar Channels plugin

Goal: broadcast events to WebSocket clients through channels with an optional broker.

## Method

Create the plugin with a backend and channels, then register it in `plugins`:

```python
from litestar.channels import ChannelsPlugin
from litestar.channels.backends.memory import MemoryChannelsBackend

channels_plugin = ChannelsPlugin(backend=MemoryChannelsBackend(history=20), channels=["foo", "bar"])
app = Litestar([handler], plugins=[channels_plugin])
```

- The plugin is injectable as a dependency named `channels` (`channels: ChannelsPlugin` or `NamedDependency[ChannelsPlugin]`).
- Channels are fixed via `channels=[...]`, or created on first subscription with `arbitrary_channels_allowed=True`. Otherwise publishing or subscribing to an unknown channel raises `ChannelsException`.
- Publish: `channels.publish({"message": "Hello"}, "general")` is non-blocking; it enqueues, so the event may not be in the backend yet, but on shutdown the plugin waits for queues to empty. `await channels.wait_published(...)` skips the internal queue and publishes directly.
- Subscribe (prefer the context manager, which unsubscribes for you):

```python
async with channels.start_subscription(["foo", "bar"]) as subscriber:
    ...
```

Manual alternative: `subscriber = await channels.subscribe([...])` then `await channels.unsubscribe(subscriber)` in `finally`; `channels.unsubscribe(subscriber, ["foo"])` drops one channel.
- Consume events (always bytes): `subscriber.iter_events()` (infinite async generator) or `subscriber.run_in_background(socket.send_text)` as an async context manager, which frees the handler to also receive from the socket. `join=False` cancels the task on exit.
- History (backend-dependent): `await channels.put_subscriber_history(subscriber, ["some_channel"], limit=10)`.
- Backpressure: backlog is unlimited by default. `ChannelsPlugin(backend=..., max_backlog=1000, backlog_strategy="backoff")` drops new messages when full; `"dropleft"` evicts the oldest.
- Backends: `MemoryChannelsBackend` (single process, testing), `RedisChannelsPubSubBackend` (low latency; recommended when history is not needed), `RedisChannelsStreamBackend` (use when history is needed), `AsyncPgChannelsBackend`, `PsycoPgChannelsBackend` (psycopg 3.2.4+).
- Generate websocket handlers per channel with `create_ws_route_handlers=True`; send history on connect with `ws_handler_send_history=10` (and `history=10` on the backend). With `arbitrary_channels_allowed`, one handler with a channel path parameter is generated.

## Gotchas

- Iterating `iter_events` with WebSockets can suspend forever: `WebSocketDisconnect` is raised only after the ASGI event is received, so if the client disconnects and nothing is received, no send happens to break the loop.

## Checked

2026-11-07. Read the full cited page(s) (usage/channels.html) and the example files they include, and confirmed the claims in this skill against that text. Reworded the Redis pub/sub backend note to the page's own wording.

Method: documentation only; no commands were run.
