---
id: computing-software.messaging-and-integration.ntfy.action-http-broadcast
name: action-http-broadcast
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, actions, http-action, broadcast, cors]
level: advanced
status: docs-checked
description: "Use ntfy http and broadcast action buttons: defaults, the headers and body keys, Android intents, and the web app CORS requirement."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/publish.md
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/subscribe/web.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# http and broadcast actions

## Formats

```
http, <label>, <url>[, method=<method>][, headers.<header>=<value>][, body=<body>][, clear=true]
broadcast, <label>[, extras.<param>=<value>][, intent=<intent>][, clear=true]
```

## http

- Default method is POST, not GET; set `method=`.
- Default body is empty.
- `clear=true` clears the notification only if the request succeeds.

```
curl -d "Turn down the A/C?" \
  -H "Actions: http, Turn down, https://api.nest.com/, body='{\"temperature\": 65}'" \
  ntfy.sh/myhome
```

## broadcast (Android only)

- Default intent: `io.heckel.ntfy.USER_ACTION`.
- Only string extras are supported; pass as `extras.<param>=<value>` in the header, or as a map in JSON.

## Web app caveat

HTTP actions use fetch and are subject to CORS. The target must answer the preflight with `Access-Control-Allow-Origin` set to the ntfy origin (for example `https://ntfy.sh`) or `*`.

## Checked

2026-11-04. Confirmed against the ntfy publish page (Send HTTP request, Send Android broadcast) and the web app page: formats, POST default, empty body default, clear-on-success, default intent `io.heckel.ntfy.USER_ACTION`, string-only extras, CORS limit and allowed origin header. Removed: the Verify step.
Method: documentation only; no commands were run.
