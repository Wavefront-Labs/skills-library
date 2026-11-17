---
id: computing-software.software-engineering.dart.dart-websocket-sockets
name: dart-websocket-sockets
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-sockets, websocket-sockets]
level: advanced
status: draft
description: "Use WebSocket from dart:io or package:web_socket_channel and raw Socket/ServerSocket with framing and backpressure."
sources: ["https://dart.dev/language", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# WebSocket clients and servers, raw sockets
- `final ws = await WebSocket.connect('wss://x.test/ws'); ws.listen(onMsg); ws.add('hi');`; `package:web_socket_channel` works on web too.
- Raw TCP: `Socket.connect(host, port)`, `ServerSocket.bind(InternetAddress.loopbackIPv4, 8080)`; a TCP stream has no message boundaries, so add length-prefix framing.
- Set `pingInterval` for WebSockets to detect dead peers; handle `onDone` and reconnect with backoff.
- Respect backpressure: use `Socket.flush()`/`await` before queuing large data.
Verify: an echo server test that sends split and merged messages.
