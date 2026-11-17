---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.forward-auth-plugin
name: forward-auth-plugin
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, forward-auth, external-auth, authentication, auth-service, plugin]
level: advanced
status: docs-checked
description: "Delegate authentication to an external service with APISIX forward-auth: uri, request_method, header forwarding lists, timeouts, status_on_error and allow_degradation."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/forward-auth.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# forward-auth plugin

Attributes and defaults:
- `uri` (required): auth service URI.
- `request_method`: `GET` (or `POST`); `ssl_verify`: true.
- `request_headers`: client headers sent to the auth service.
- `upstream_headers`: auth response headers passed to the upstream.
- `client_headers`: auth response headers returned to the client on failure.
- `extra_headers`: object; NGINX variables allowed.
- `timeout`: 3000 ms (1-60000); `keepalive`: true; `keepalive_timeout`: 60000; `keepalive_pool`: 5.
- `max_req_body_size`: 67108864.
- `allow_degradation`: false; `status_on_error`: 403.

```json
{
  "uri": "http://127.0.0.1:9080/auth",
  "request_headers": ["Authorization"],
  "upstream_headers": ["X-User-ID"],
  "client_headers": ["X-Forward-Auth"],
  "extra_headers": { "X-Forwarded-Upstream-Uri": "$upstream_uri" },
  "status_on_error": 403
}
```

Behavior:
- APISIX sends `X-Forwarded-Proto`, `-Method`, `-Host`, `-Uri` and `-For` describing the original request.
- On success the request continues with the listed `upstream_headers`; client-supplied values of those headers are removed.
- On failure the client gets the auth service's status and the `client_headers`.
- Network errors return `status_on_error`.
- With `POST`, request bodies over `max_req_body_size` are rejected with 413.
- After a `proxy-rewrite`, pass `$upstream_uri` via `extra_headers`.

## Checked

2026-11-04. Confirmed against the APISIX forward-auth plugin page: all attribute defaults and ranges, the X-Forwarded-* headers, upstream_headers removal of client-supplied values, client_headers on failure, status_on_error, the 413 limit, the $upstream_uri note. Nothing removed.

Method: documentation only; no commands were run.
