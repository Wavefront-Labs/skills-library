---
id: computing-software.web-development.frontend-development.websocket-client-reconnect-and-heartbeat
name: websocket-client-reconnect-and-heartbeat
category: computing-software
field: web-development
product: frontend-development
tags: [fetch-api, browser-networking, websocket-client, websocket-reconnect, heartbeat, backpressure, bufferedamount, real-time]
level: practitioner
status: docs-checked
description: "A production WebSocket client: reconnect with backoff and jitter, heartbeats to detect dead connections, resubscribe and resync, and bufferedAmount backpressure."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/WebSocket
  - https://www.rfc-editor.org/rfc/rfc6455
  - https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_client_applications
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WebSocket client: reconnect and heartbeat

**Goal:** a real-time connection that survives network changes, detects silent drops, and never loses or duplicates state after reconnecting.

## 1. Reconnect with backoff
```js
function connect(url, onMessage) {
  let ws, attempt = 0, closedByUs = false, pingTimer;
  const open = () => {
    ws = new WebSocket(url);
    ws.onopen = () => { attempt = 0; resubscribeAndResync(ws); heartbeat(); };
    ws.onmessage = (e) => { if (e.data === 'pong') return; onMessage(JSON.parse(e.data)); };
    ws.onclose = (e) => {
      clearInterval(pingTimer);
      if (closedByUs || e.code === 4001 /* app: auth rejected */) return;
      const delay = Math.min(30_000, 500 * 2 ** attempt++) * (0.5 + Math.random());   // jitter avoids thundering herd
      setTimeout(open, delay);
    };
  };
  const heartbeat = () => {
    let lastPong = Date.now();
    ws.addEventListener('message', (e) => { if (e.data === 'pong') lastPong = Date.now(); });
    pingTimer = setInterval(() => {
      if (Date.now() - lastPong > 45_000) return ws.close(4000, 'heartbeat timeout');   // triggers reconnect
      if (ws.readyState === WebSocket.OPEN) ws.send('ping');
    }, 15_000);
  };
  open();
  return { send: (m) => ws.readyState === 1 && ws.send(JSON.stringify(m)), close: () => { closedByUs = true; ws.close(1000); } };
}
```
The browser `WebSocket` API has no method for sending protocol-level Ping/Pong frames (MDN's client guide uses an application-level "ping" text message), so use an application-level ping and have your server reply. Without a heartbeat, a silently dropped connection (laptop sleep, network switch) may not be noticed until the next send fails. Close codes passed to `close()` must be `1000` or in the range `3000`-`4999`, and RFC 6455 reserves `4000`-`4999` for private use, so the codes above are valid application codes.

## 2. Resync after reconnect
Messages sent while disconnected are lost. On every open: re-authenticate, re-subscribe to channels, and fetch missed events (send last seen sequence number/timestamp, or refetch state over HTTP).

## 3. Auth
The `WebSocket()` constructor takes only a URL and sub-protocols, so there is no way to add an `Authorization` header. Use the session cookie (RFC 6455 section 10.2: servers that accept only certain origins SHOULD verify the `Origin` header, which also guards against cross-site WebSocket hijacking), or a short-lived token in the first message (preferred over the query string, which tends to end up in logs).

## 4. Backpressure
`ws.send` does not block; `bufferedAmount` is the number of bytes queued by `send()` and not yet transmitted to the network (it resets to zero once everything is sent, and not when the connection closes). For large or fast streams, pause producing while `bufferedAmount` exceeds a threshold. MDN notes that the `WebSocket` interface has no backpressure for incoming messages.

## 5. Also reconnect on
`online` event and `visibilitychange` to visible (mobile browsers kill sockets in background).

## Verify
- [ ] Kill the server: client retries with growing, jittered delays; resumes on restart with no missed data.
- [ ] Toggle airplane mode: the dead connection is detected within your heartbeat timeout (45 s in this example).
- [ ] Server rejects connections from foreign `Origin`.

## Checked

Checked 2026-10-26 against MDN WebSocket, WebSocket.close(), WebSocket.bufferedAmount, WebSocket() constructor, the WebSockets API overview and Writing WebSocket client applications (mdn/content main) and RFC 6455 (sections 5.5, 7.4.2, 10.2): close-code ranges, bufferedAmount semantics, application-level ping in MDN's guide, no incoming-message backpressure, and server-side Origin verification. The reconnect delays and heartbeat intervals are design choices, not documented values. Removed the unconfirmed 'looks open for minutes' claim.

Method: documentation only; no commands were run.
