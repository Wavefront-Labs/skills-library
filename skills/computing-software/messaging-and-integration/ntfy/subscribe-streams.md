---
id: computing-software.messaging-and-integration.ntfy.subscribe-streams
name: subscribe-streams
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, subscribe, json-stream, sse, websocket]
level: practitioner
status: docs-checked
description: "Subscribe to an ntfy topic over HTTP JSON stream, SSE, raw stream or WebSocket, and pick the right one."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/subscribe/api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subscribing over the API

The connection stays open indefinitely.

| Endpoint | Format |
|---|---|
| `<topic>/json` | one JSON object per line (`application/x-ndjson`); recommended for almost all languages |
| `<topic>/sse` | Server-Sent Events for `EventSource`; much easier than JSON for JavaScript |
| `<topic>/raw` | plain text, body only (no title, priority, tags); keepalives are empty lines |
| `<topic>/ws` | WebSocket, JSON objects like the JSON stream |

```
curl -s ntfy.sh/mytopic/json
curl -s ntfy.sh/mytopic/sse
curl -s ntfy.sh/mytopic/raw
websocat wss://ntfy.sh/mytopic/ws
```

## Gotchas

- `raw` loses metadata; use `json` if you need priority or tags.
- Through a reverse proxy, forward `Upgrade` and `Connection` for WebSockets and disable proxy buffering as in the nginx example in the config page; see behind-proxy.
- Authentication is basic auth, a bearer token or the `auth` query parameter.
- The stream also carries `open`, `keepalive`, `message_delete`, `message_clear` and `poll_request` events; typically you are only interested in `message`.

## Checked

2026-11-04. Confirmed against the ntfy subscribe API page (HTTP stream endpoints, raw stream, WebSockets, auth) and config page (nginx proxy example forwards Upgrade/Connection, buffering off). Removed: the stream-hang claim and the Verify step.
Method: documentation only; no commands were run.
