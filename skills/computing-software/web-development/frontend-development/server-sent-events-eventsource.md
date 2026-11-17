---
id: computing-software.web-development.frontend-development.server-sent-events-eventsource
name: server-sent-events-eventsource
category: computing-software
field: web-development
product: frontend-development
tags: [fetch-api, browser-networking, server-sent-events, eventsource, sse, last-event-id, text-event-stream, real-time]
level: practitioner
status: docs-checked
description: "Server-sent events with EventSource: the text/event-stream format, auto-reconnect with Last-Event-ID, proxy buffering, connection limits and auth options."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events
  - https://html.spec.whatwg.org/multipage/server-sent-events.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Server-sent events (EventSource)

**Goal:** one-way server-to-browser streaming over plain HTTP with built-in reconnection and resume.

## 1. When to choose SSE over WebSockets
Server pushes, client rarely sends (notifications, progress, live feeds, LLM token streams). Works through HTTP infrastructure, auto-reconnects, resumes by event id. Text only (UTF-8).

## 2. Wire format
Response `Content-Type: text/event-stream`, `Cache-Control: no-cache`, kept open:
```
id: 1042
event: order-updated
data: {"id":42,"status":"shipped"}

: comment line used as keepalive

retry: 5000
```
Each event ends with a blank line. Multiple `data:` lines are joined with `\n`.

## 3. Client
```js
const es = new EventSource('/api/events', { withCredentials: true });  // withCredentials for cross-origin cookies
es.addEventListener('order-updated', (e) => update(JSON.parse(e.data)));
es.onmessage = (e) => {};       // only events without an `event:` field
es.onerror = () => { if (es.readyState === EventSource.CLOSED) showOffline(); };   // CONNECTING = retrying automatically
```
On reconnect the browser sends `Last-Event-ID` with the last `id:` it saw; the server replays events after it. Without ids you lose events during the gap.

## 4. Server notes
- Flush after each event; disable proxy buffering (`X-Accel-Buffering: no` for nginx) and response compression that buffers.
- Send a comment line (starting with a colon) periodically as a keep-alive so idle proxies and load balancers don't close the connection; choose the interval from your proxies' idle timeouts.
- To stop the client from reconnecting, respond with HTTP 204 No Content (WHATWG HTML spec); a client reconnects whenever the connection is closed otherwise.
- In Express: set headers, `res.flushHeaders()`, `res.write(...)`, clean up on `req.on('close')`.

## 5. Limits and auth
- When not used over HTTP/2, MDN says the number of open SSE connections is limited per browser to a very low number (6), which hurts when many tabs are open (marked "Won't fix" in Chrome and Firefox). Use HTTP/2 or share one connection across tabs via a SharedWorker or a BroadcastChannel/Web Locks leader.
- EventSource can't send custom headers. Use cookies, or use `fetch` + a stream parser (e.g. `@microsoft/fetch-event-source`) when you need `Authorization` headers or POST bodies.

## Verify
- [ ] A raw HTTP client that does not buffer shows events arriving one by one.
- [ ] Restart the server: client reconnects and receives events missed since `Last-Event-ID`.
- [ ] Many tabs open over HTTP/2 do not block page loads.

## Checked

Checked 2026-10-26 against MDN Using server-sent events and EventSource() (mdn/content main) and the WHATWG HTML Living Standard section 9.2 Server-sent events: `text/event-stream`, UTF-8, comment lines as keep-alive, `retry`, `Last-Event-ID` header (section 9.2.4), 204 stopping reconnection, `withCredentials`, `X-Accel-Buffering: no` in MDN's server example, and the six-connection limit without HTTP/2. The `@microsoft/fetch-event-source` package exists (Azure/fetch-event-source package.json, version 2.0.1). Removed the unconfirmed 15-30 s interval and `curl -N` check.

Method: documentation only; no commands were run.
