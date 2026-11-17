---
id: computing-software.web-development.litestar.litestar-websocket-listeners
name: litestar-websocket-listeners
category: computing-software
field: web-development
product: litestar
tags: [litestar, websocket, websocket-listener, websocket-stream, transport-mode, dependency-injection]
level: practitioner
status: docs-checked
description: "Build Litestar websocket_listener handlers, class-based WebsocketListener, receive_mode and send_mode, dependency injection, and websocket_stream."
sources: [https://docs.litestar.dev/latest/usage/websockets.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar WebSocket listeners and streams

Goal: handle WebSockets event-style without writing the receive loop yourself.

## Method

Pick the interface: low-level `websocket` handler; `websocket_listener` / `WebsocketListener` (reactive, serialization and DTO support, may be sync); `websocket_stream` and `send_websocket_stream` (proactive, push data).

Listener:

```python
from litestar import Litestar, websocket_listener

@websocket_listener("/")
async def handler(data: str) -> str:
    return data

app = Litestar([handler])
```

- Receive: `data` is parsed per its annotation (`str`, `bytes`, or `dict`/`list` as JSON). Default is JSON unless `data` is annotated `str` or `bytes`. JSON is parsed but not validated.
- Send: return the value; `str` and `bytes` go as-is, everything else is JSON-serialized (dataclasses, TypedDict, NamedTuple, msgspec.Struct, DTOs).
- Transport modes are `text` (default) and `binary`, set independently: `@websocket_listener("/", receive_mode="binary")` and `send_mode="binary"`. Modes govern wire transport, not `str` vs `bytes`. A listener set to binary will not respond to text-channel events.
- Dependencies: `dependencies={"client_count": Provide(socket_client_count)}` with `client_count: NamedDependency[int]`. They are evaluated once per connection (at handler level); code after a `yield` runs after the connection closes.
- Raw socket: add `socket: WebSocket`; the handler must be async to use its async methods.
- Custom accept: `connection_accept_handler=accept_connection` where it awaits `socket.accept(headers={...})`. Default awaits `WebSocket.accept()` with no arguments.
- Class based: subclass `litestar.handlers.WebsocketListener`, set `path`, implement `on_receive`, optionally `on_accept` and `on_disconnect`.
- Custom `websocket_class` (since 2.7.0) can be set on any layer; the layer closest to the handler wins.

Stream:

```python
@websocket_stream("/")
async def ping() -> AsyncGenerator[float, None]:
    while True:
        yield time.time()
        await asyncio.sleep(0.5)
```

## Gotchas

- Streams listen for client disconnect in the background; receiving data then raises unless `allow_data_discard=True`.
- To stream and receive at once, use `send_websocket_stream` with a `websocket` handler or listener; with `listen_for_disconnect=False` you must receive the disconnect yourself, else the stream ends only when the generator is exhausted.
- Stream dependencies live as long as the generator, so a lock or connection acquired in one is held until the client disconnects; acquire inside the generator instead.

## Checked

2026-11-07. Read the full cited page(s) (usage/websockets.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
