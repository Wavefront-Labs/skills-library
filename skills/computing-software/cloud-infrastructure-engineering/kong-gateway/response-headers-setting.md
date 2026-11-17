---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.response-headers-setting
name: response-headers-setting
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, headers, headers-upstream, latency-tokens, kong-conf, x-kong-request-id]
level: practitioner
status: docs-checked
description: "Control which headers Kong injects into client responses and upstream requests with headers and headers_upstream, plus allow_debug_header."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong.conf.default
  - https://developer.konghq.com/gateway/logs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# headers and headers_upstream

| Setting | Default | Controls |
|---|---|---|
| `headers` | `server_tokens, latency_tokens, X-Kong-Request-Id` | headers Kong injects in client responses |
| `headers_upstream` | `X-Kong-Request-Id` | headers Kong injects in requests to upstream; the only accepted value is `X-Kong-Request-Id` |
| `allow_debug_header` | `off` | enables the `Kong-Debug` header function |
| `error_default_type` | `text/plain` | default MIME type when the request has no `Accept` header and Nginx returns an error (`text/plain`, `text/html`, `application/json`, `application/xml`) |

Set `headers` to `off` to stop Kong injecting any of its response headers; plugins can still inject their own. `server_tokens` means `Server` plus `Via`; `latency_tokens` means the Proxy, Response, Admin and Upstream latency headers.

The `X-Kong-Request-Id` header is a unique identifier for each client request and can be used to match requests to their error log entries.

With `allow_debug_header` on, Kong adds `Kong-Route-Id`, `Kong-Route-Name`, `Kong-Service-Id` and `Kong-Service-Name` response headers when the client request carries `Kong-Debug: 1`.

## Checked

2026-11-04. Confirmed against kong.conf.default and the Kong Gateway logs page: defaults, header meanings, `off` semantics, request ID use, debug header behaviour and `error_default_type`. Removed the claim about why debug is off by default and the correlation-id plugin pointer, neither of which the sources state.
Method: documentation only; no commands were run.
