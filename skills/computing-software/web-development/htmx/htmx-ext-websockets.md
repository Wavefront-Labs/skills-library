---
id: computing-software.web-development.htmx.htmx-ext-websockets
name: htmx-ext-websockets
category: computing-software
field: web-development
product: htmx
tags: [htmx, extensions, websockets, ws-connect, ws-send, reconnection, oob]
level: practitioner
status: docs-checked
description: "Two-way WebSocket UIs with the htmx ws extension: ws-connect, ws-send, OOB-style incoming swaps, JSON outgoing messages, reconnect delay, config options, events and socketWrapper."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/extensions/ws.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: bi-directional server communication straight from HTML.

Install: core htmx first, then `https://cdn.jsdelivr.net/npm/htmx-ext-ws@2.0.4`, then `hx-ext="ws"` (npm: `htmx-ext-ws`, bundle `dist/ws.js`).

```html
<div hx-ext="ws" ws-connect="/chatroom">
  <div id="notifications"></div>
  <div id="chat_room">...</div>
  <form id="form" ws-send>
    <input name="chat_message">
  </form>
</div>
```

- `ws-connect="<url>"` or `"<prefix>:<url>"` with prefix `ws` or `wss`. With no prefix, htmx uses the page location's scheme, host and port, so cookies are sent.
- `ws-send` sends a message to the nearest enclosing socket when the element's trigger fires (natural event or `hx-trigger`). A form's values are serialised as JSON and include a `HEADERS` field with the usual htmx request headers.

Incoming messages are parsed as HTML and swapped by element `id` using the same logic as out-of-band swaps, defaulting to `hx-swap-oob="true"`. To change the method, say so in the message:

```html
<form id="form">...</form>
<div id="notifications" hx-swap-oob="beforeend">New message received</div>
<div id="chat_room" hx-swap-oob="morphdom">...</div>
```

Reconnection. On Abnormal Closure, Service Restart or Try Again Later, the extension reconnects with a full-jitter exponential backoff. Replace it via `htmx.config.wsReconnectDelay = function (retryCount) { return retryCount * 1000 }` (milliseconds). Messages sent while the socket is not OPEN are queued in memory and sent after reconnect.

Config options: `createWebSocket` (factory returning a `WebSocket`) and `wsBinaryType` (default `blob`).

Events: `htmx:wsConnecting`, `htmx:wsOpen`, `htmx:wsClose`, `htmx:wsError`, `htmx:wsBeforeMessage` (cancel to stop processing; `detail.message`), `htmx:wsAfterMessage`, `htmx:wsConfigSend`, `htmx:wsBeforeSend` (cancel to discard), `htmx:wsAfterSend`.
- In `htmx:wsConfigSend` you can edit `detail.parameters` and `detail.headers`, or set `detail.messageBody` to override JSON serialisation (for XML or MessagePack); cancelling sends nothing.

`detail.socketWrapper` on every event exposes `send(message, fromElt)` (queues if not open), `sendImmediately(message, fromElt)` (bypasses the queue, may fail) and `queue` (array of pending messages).

Migrating from htmx 1: `hx-ws=""` becomes `hx-ext="ws"`, `hx-ws="connect:<url>"` becomes `ws-connect="<url>"`, `hx-ws="send"` becomes `ws-send=""`.

## Checked

2026-11-07. Confirmed on extensions/ws.md (`ws-connect` forms and prefixes, `ws-send`, JSON serialisation with `HEADERS`, id-based out-of-band style swaps, `htmx.config.wsReconnectDelay`, queueing, `createWebSocket` and `wsBinaryType`, all nine events and their cancel behaviour, `socketWrapper` members, migration table).
Removed: the invented Verify step.
Method: documentation only; no commands were run.
