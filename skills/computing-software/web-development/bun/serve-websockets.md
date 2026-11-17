---
id: computing-software.web-development.bun.serve-websockets
name: serve-websockets
category: computing-software
field: web-development
product: bun
tags: [websocket-server, pub-sub, backpressure, origin-check]
level: advanced
status: docs-checked
description: "Build WebSocket servers in Bun.serve: upgrade, typed data, pub/sub topics, payload and backpressure limits, compression, close codes and origin checks."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/runtime/http/websockets.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
Bun.serve({
  fetch(req, server) {
    const origin = req.headers.get("origin");
    if (origin && origin !== "https://app.example.com") return new Response("Forbidden", { status: 403 });
    if (server.upgrade(req, { data: { room: "general" } })) return; // undefined on success
    return new Response("Upgrade failed", { status: 400 });
  },
  websocket: {
    data: {} as { room: string },             // types ws.data (replaces Bun.serve<T>())
    open(ws) { ws.subscribe("chat"); },
    message(ws, msg) { ws.publish("chat", msg); }, // publish excludes the sender
    maxPayloadLength: 1024 * 1024, perMessageDeflate: true,
  },
});
```

Handlers: `open`, `message`, `close`, `drain`, `ping`, `pong`, `error(error, ws)`. `server.publish(topic, msg)` reaches everyone.

Defaults: `idleTimeout` 120 s (0-960), `maxPayloadLength` 16 MB (over limit closes with 1009), `backpressureLimit` 16 MB.

Gotchas:
- Cookies ride the handshake, so verify `Origin` against an allowlist before `upgrade()` (cross-site hijacking).
- `send()` returns -1 when queued (wait for `drain`), 0 when dropped.
- `server.stop()` leaves sockets open; `stop(true)` closes with 1001.
- Rejected `async` handlers do not reach `error`. Close reasons truncate at 123 bytes.

## Checked

2026-11-04. Confirmed against the Bun docs page runtime/http/websockets: upgrade pattern, handler list and error(error, ws) argument order, data typing via the websocket data property, publish excluding the sender and server.publish reaching all, idleTimeout default 120 and range 0-960, maxPayloadLength and backpressureLimit 16 MB, close 1009, send() return values, drain, stop versus stop(true) with 1001, async handler rejection not reaching error, reason truncation at 123 bytes, and the Origin allowlist warning. Replaced the skill's example origin check, which compared the request URL origin, with a check of the Origin header as the page shows.
Method: documentation only; no commands were run.
