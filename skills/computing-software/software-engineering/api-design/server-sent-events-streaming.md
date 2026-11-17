---
id: computing-software.software-engineering.api-design.server-sent-events-streaming
name: server-sent-events-streaming
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, server-sent-events, sse, eventsource, text-event-stream, last-event-id, streaming, real-time]
level: practitioner
status: docs-checked
description: "Stream one-way events with Server-Sent Events: wire format, event ids and Last-Event-ID resume, heartbeats, proxy buffering pitfalls and when to choose WebSockets."
sources: ["https://html.spec.whatwg.org/multipage/server-sent-events.html", "https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Server-Sent Events (SSE)

A long-lived response with `Content-Type: text/event-stream`, consumed in browsers with `EventSource`, which reconnects automatically when the connection closes. One-directional (server to client): a client cannot send events back over it.

## Wire format
```http
HTTP/1.1 200 OK
Content-Type: text/event-stream
Cache-Control: no-cache

id: 42
event: order.updated
retry: 5000
data: {"orderId":"o_1","status":"shipped"}

: heartbeat comment

```
Fields: `id`, `event` (name; messages without one are `message` events), `data` (consecutive `data:` lines are joined with a newline), `retry` (reconnection time in ms; ignored unless an integer). A line starting with `:` is a comment; other field names are ignored; a line without a colon is a field name with an empty value. A blank line ends an event, and an event not followed by a blank line is discarded. The stream is always UTF-8. One space after the colon is ignored.

## Resume
When the browser reconnects it sends the last event id it saw in a `Last-Event-ID` request header (the value is any UTF-8 string without NUL, LF or CR); replay events after that id from a buffer or log. Setting an empty `id:` resets it so no header is sent. Without ids, clients miss events during drops.

## Server tips
- Send a comment line every 15 seconds or so so legacy proxies that drop idle connections keep the stream open (the spec's authoring note).
- Disable response buffering and flush after each event; the MDN PHP example sends `X-Accel-Buffering: no` (an nginx directive) and calls `flush()` in its loop.
- Over HTTP/1.1 browsers allow about 6 SSE connections per browser and domain across all tabs; over HTTP/2 the stream limit is negotiated (default 100 per MDN).
- Reply with HTTP 204 No Content to tell the client to stop reconnecting. Redirects 301 and 307 are followed.
- The spec warns that HTTP chunking done by a layer unaware of the timing needs can hurt reliability; chunking can be disabled for event streams.
- Detect a closed client connection and break out of your send loop; MDN's example does this with `connection_aborted()`.

## SSE vs WebSocket
MDN describes SSE as one-way and WebSockets as two-way. Use SSE for notifications, progress and live feeds; choose WebSockets when the client must send frequent messages.

## Gotchas
- Compression or proxy middleware that buffers will hold events back; test through your real path.
- The client calls `close()` to stop; without it a dropped connection is restarted.
- Cross-origin streams need `new EventSource(url, { withCredentials: true })` for credentials, and access-control failures raise an `error` event.

Verify: `curl -N <url>` prints events as they occur (not in one burst), and a request carrying a `Last-Event-ID` header resumes after that id.

## Checked
2026-11-08. Confirmed against the WHATWG HTML Server-sent events section (stripped text, partially read, not in full:  the introduction, Last-Event-ID, parsing and authoring notes) and the MDN Using server-sent events guide (read in full). Removed: the `Accept: text/event-stream` curl header, the claim that `EventSource` cannot set custom headers and the `@microsoft/fetch-event-source` suggestion (not in the sources), and the 15-30 s heartbeat range (the spec says about 15 seconds).
Method: documentation only; no commands were run.
