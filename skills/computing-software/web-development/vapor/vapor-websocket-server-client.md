---
id: computing-software.web-development.vapor.vapor-websocket-server-client
name: vapor-websocket-server-client
category: computing-software
field: web-development
product: vapor
tags: [vapor,websockets,websocket,realtime,ontext,swift,async-await]
level: practitioner
status: docs-checked
description: "Add WebSocket routes to a Vapor app, connect as a client, send and receive text/binary messages, close, and handle ping/pong."
sources:
  - https://docs.vapor.codes/advanced/websockets/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: two-way messaging with Vapor's WebSocket API.

**Server.** Use `webSocket` like `get`/`post`; routes can be grouped and protected by middleware.

```swift
app.webSocket("echo") { req, ws in
    // Connected WebSocket.
}
```

**Client.** `WebSocket.connect` returns a future that completes when connected:

```swift
WebSocket.connect(to: "ws://echo.websocket.org", on: eventLoop) { ws in
    print(ws)
}
```

**Sending.** A `String` sends a text message (UTF-8); a `[UInt8]` sends binary.

```swift
ws.send("Hello, world")
ws.send([1, 2, 3])
```

Sending is async. Pass `promise:` (an `EventLoopPromise<Void>`) to be told when it finished or failed, or `try await ws.send(...)`.

**Receiving.**

```swift
ws.onText { ws, text in ws.send(text) }   // echo
ws.onBinary { ws, binary in print(binary) }
```

The socket is passed as the first parameter to avoid reference cycles; use it to reply.

**Closing.** `ws.close()` returns a future (accepts `promise:`, or `try await ws.close()`). `ws.onClose` is a future that completes when either side closes. `closeCode` is set on close and shows why the peer closed.

**Ping/pong.** Sent automatically by client and server to keep the connection alive; observe with `ws.onPing { ws in ... }` and `ws.onPong { ws in ... }`.

## Checked

2026-11-08: read in full the WebSockets page at docs.vapor.codes/advanced/websockets/ (server route, client connect, send, receive, close, ping/pong). Every claim was found on the cited pages; nothing needed removing.

Method: docs-only read of cited pages, 2026-11-08
