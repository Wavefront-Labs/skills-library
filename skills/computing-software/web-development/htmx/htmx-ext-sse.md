---
id: computing-software.web-development.htmx.htmx-ext-sse
name: htmx-ext-sse
category: computing-software
field: web-development
product: htmx
tags: [htmx, extensions, sse, server-sent-events, eventsource, sse-connect, sse-swap]
level: practitioner
status: docs-checked
description: "Stream server-sent events into the page with the htmx sse extension: sse-connect, sse-swap, hx-trigger sse:name, sse-close, event format, reconnection and htmx:sse* events."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/extensions/sse.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: swap server-pushed HTML into the page in real time over a one-way EventSource connection (works through proxies and firewalls; no client-to-server messages after connecting, use WebSockets for two-way).

Install: core htmx first, then `https://cdn.jsdelivr.net/npm/htmx-ext-sse@2.2.4`, then `hx-ext="sse"` on an element (npm: `htmx-ext-sse`, bundle `dist/sse.js`). With the idiomorph extension, htmx-ext-sse 2.2.4 or later is required.

Attributes
- `sse-connect="<url>"`: the SSE endpoint; must be on the same element as `hx-ext="sse"`. Query parameters work, for example `/chat-updates?friends=true&format=detailed`.
- `sse-swap="<message-name>"`: event name whose data is swapped in. Place it on or inside the `sse-connect` element. Comma-separate several names: `sse-swap="event1,event2"`.
- `hx-trigger="sse:<message-name>"`: fire a normal request when that event arrives.
- `sse-close="<message-name>"`: close the stream gracefully when that message is received.

```html
<div hx-ext="sse" sse-connect="/chatroom" sse-swap="message">updated live</div>

<div hx-ext="sse" sse-connect="/event_stream">
  <div hx-get="/chatroom" hx-trigger="sse:chatter">...</div>
</div>
```

Server message format: only an event name and data.

```txt
event: EventName
data: <div>Content to swap into your HTML page.</div>
```

Names must match exactly; an event the page is not listening for is discarded. An unnamed message arrives as `message`, so use `sse-swap="message"`; there is no catch-all.

Reconnection: besides the browser's own retry, the extension adds exponential-backoff reconnection.

Events (on `document.body`, for example `addEventListener('htmx:sseBeforeMessage', ...)`)
- `htmx:sseOpen` (`detail.elt`, `detail.source`), `htmx:sseError` (`detail.error`, `detail.source`).
- `htmx:sseBeforeMessage`: before swap; `preventDefault()` cancels the swap; `detail` is the MessageEvent.
- `htmx:sseMessage`: after swap.
- `htmx:sseClose`: `e.detail.type` is `nodeMissing`, `nodeReplaced` or `message`.

Migrating from htmx 1: `hx-sse=""` becomes `hx-ext="sse"`; `hx-sse="connect:<url>"` becomes `sse-connect`; `hx-sse="swap:Name"` becomes `sse-swap="Name"`; `hx-trigger="sse:Name"` is unchanged.

## Checked

2026-11-07. Confirmed on extensions/sse.md (the four attributes, install and 2.2.4 idiomorph note, same-element rule for `sse-connect` and `hx-ext`, query parameters, event format, `message` default and no catch-all, comma-separated `sse-swap`, `sse:` triggers, exponential-backoff reconnection, the migration table, and the `htmx:sse*` events with their detail fields and `sseClose` types).
Removed: the invented Verify step with its `text/event-stream` claim, which the page does not state.
Method: documentation only; no commands were run.
