---
id: computing-software.web-development.fastapi.websockets-endpoints
name: websockets-endpoints
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, websockets, websocket, websocketdisconnect, websocketexception, broadcast]
level: practitioner
status: docs-checked
description: "Build WebSocket endpoints in FastAPI: accept and exchange messages, use Depends and Query, raise WebSocketException, and handle WebSocketDisconnect."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/advanced/websockets.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WebSockets

## Method
- Install `websockets`.
- Declare a WebSocket route taking a `WebSocket` parameter (`from fastapi import WebSocket`, same as Starlette's). In it, `await` messages and send replies; text, binary and JSON are supported.
- The docs example connects from a simple HTML page; in production use your frontend framework or native client.
- Use `Depends`, `Security`, `Cookie`, `Header`, `Path` and `Query` as in normal path operations.
- Raising `HTTPException` makes no sense on a WebSocket; raise `WebSocketException` with a closing code from RFC 6455 section 7.4.1.
- When a connection closes, `await websocket.receive_text()` raises `WebSocketDisconnect`; catch it, e.g. to tell other clients someone left.

## Limits
The docs chat example keeps connections in an in-memory list, so it works only in a single process. For something sturdier (Redis, PostgreSQL) the docs point to encode/broadcaster.

## More
Starlette docs cover the `WebSocket` class and class-based `WebSocketEndpoint`.

## Verify
Open the page in two tabs, send messages, close one, confirm the other is notified.

## Checked

Read the full advanced/websockets.md source page. Confirmed installing websockets, the WebSocket import, text/binary/JSON, Depends/Security/Cookie/Header/Path/Query support, WebSocketException with RFC 6455 section 7.4.1 codes, WebSocketDisconnect from receive_text, the in-memory single-process limit, encode/broadcaster, and the Starlette references. No claims removed.

Method: docs-only read of cited pages, 2026-11-08
