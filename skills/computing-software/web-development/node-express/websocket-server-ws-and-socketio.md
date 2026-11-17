---
id: computing-software.web-development.node-express.websocket-server-ws-and-socketio
name: websocket-server-ws-and-socketio
category: computing-software
field: web-development
product: node-express
tags: [rest-api, websocket-server, socket-io, websockets, real-time, node, cross-site-websocket-hijacking]
level: practitioner
status: verified
description: "Running WebSocket servers in Node with ws or Socket.IO: authentication on upgrade, origin checks, heartbeats, backpressure, scaling across instances, and proxy configuration."
sources:
  - https://github.com/websockets/ws
  - https://socket.io/docs/v4/
  - https://www.rfc-editor.org/rfc/rfc6455
  - https://cheatsheetseries.owasp.org/cheatsheets/WebSocket_Security_Cheat_Sheet.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# WebSockets on the server (ws / Socket.IO)

## 1. Choose
- **ws**: raw RFC 6455 WebSocket, minimal and fast; you build rooms, reconnection, acks.
- **Socket.IO**: its own protocol on top (not interoperable with plain WebSocket clients) with rooms, namespaces, acks, auto-reconnect, HTTP long-polling fallback and adapters for multi-node.
- Consider SSE for server-to-client only streams (simpler, HTTP semantics).

## 2. ws with auth on upgrade
```js
import { WebSocketServer } from "ws";
const wss = new WebSocketServer({ noServer: true, maxPayload: 64 * 1024 });
server.on("upgrade", async (req, socket, head) => {
  try {
    if (!ALLOWED_ORIGINS.has(req.headers.origin)) throw new Error("origin");   // cross-site WebSocket hijacking defence
    const user = await authenticate(req);                                      // session cookie or short-lived token
    wss.handleUpgrade(req, socket, head, ws => { ws.user = user; wss.emit("connection", ws, req); });
  } catch { socket.write("HTTP/1.1 401 Unauthorized\r\n\r\n"); socket.destroy(); }
});
```
- The upgrade code above was run with ws 8.22: a wrong or missing `Origin` got `401` (so non-browser clients without an Origin are refused too), a 70 KiB message with `maxPayload` 64 KiB closed the socket with code 1009 (the server also emits `WS_ERR_UNSUPPORTED_MESSAGE_LENGTH`; attach an `error` listener), the heartbeat loop terminated a client that never answered pings, and `ws.close(1012, "service restart")` reached the client as 1012 (1012 is "Service Restart" in the IANA WebSocket close code registry).
- Browsers can't set custom headers on WebSocket - use cookies (check Origin!) or a short-lived token in the first message/subprotocol. Avoid long-lived tokens in the query string (logged by proxies).
- Re-check authorization per message/action, not just at connect; handle token expiry.

## 3. Heartbeats and cleanup
```js
setInterval(() => { for (const ws of wss.clients) { if (!ws.isAlive) { ws.terminate(); continue; } ws.isAlive = false; ws.ping(); } }, 30_000);
wss.on("connection", ws => { ws.isAlive = true; ws.on("pong", () => (ws.isAlive = true)); });
```
Dead TCP connections otherwise linger (mobile networks). Socket.IO has `pingInterval`/`pingTimeout` built in.

## 4. Backpressure and limits
- Check `ws.bufferedAmount` before sending to slow clients; drop or disconnect when over a threshold.
- `maxPayload`, per-connection message rate limits, max connections per user/IP.
- Validate every incoming message with a schema.

## 5. Scaling
- Each instance only knows its own sockets: fan out via Redis pub/sub (Socket.IO `@socket.io/redis-adapter` or streams adapter), NATS, or a managed service.
- Load balancers need WebSocket support and long idle timeouts; Socket.IO with polling fallback needs sticky sessions.
- nginx: `proxy_http_version 1.1; proxy_set_header Upgrade $http_upgrade; proxy_set_header Connection "upgrade"; proxy_read_timeout 3600s;`.
- Graceful deploys: on SIGTERM stop accepting, send close frame (code 1012 service restart), let clients reconnect with jitter.

## Verify
Load test (k6/Artillery websocket scenarios) with reconnect storms; cross-origin connection attempt rejected; killed client connections are cleaned within one heartbeat interval.
