---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.http-log
name: http-log
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, http-log, http-endpoint, log-queue, plugins, logging]
level: practitioner
status: docs-checked
description: "http-log plugin: http_endpoint, method POST/PUT/PATCH, content_type, timeout 10000, keepalive 60000, custom headers, and the queue settings replacing deprecated fields."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong/plugins/http-log/schema.lua
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# http-log

| Field | Default | Notes |
|---|---|---|
| `http_endpoint` | required | URL that receives the log entries |
| `method` | `POST` | `POST`, `PUT` or `PATCH` |
| `content_type` | `application/json` | or `application/json; charset=utf-8` |
| `timeout` | `10000` ms | time to wait when sending |
| `keepalive` | `60000` ms | idle connection lifetime |
| `headers` | none | extra headers; cannot be `Host`, `Content-Length` or `Content-Type` |
| `queue` | defaults | batching and retry settings |
| `custom_fields_by_lua` | none | Lua code to change logged fields |

Deprecated (removed in 4.0): `retry_count` (use `queue.max_retry_time`), `queue_size` (use `queue.max_batch_size`), `flush_timeout` (use `queue.max_coalescing_delay`).

If `http_endpoint` contains credentials in the URL (userinfo), `headers` cannot also contain `Authorization`.

Encryption of `http_endpoint` is Enterprise only and has no effect in open source.

## Checked

2026-11-04. Confirmed against the http-log schema.lua: http_endpoint required and encrypted (Enterprise only), method POST/PUT/PATCH, content_type values, timeout 10000, keepalive 60000, forbidden Host/Content-Length/Content-Type headers, the userinfo plus Authorization validator, queue, custom_fields_by_lua, and the three deprecations removed in 4.0 with their replacements.

Method: documentation only; no commands were run.
