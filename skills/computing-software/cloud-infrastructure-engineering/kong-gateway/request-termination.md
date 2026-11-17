---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.request-termination
name: request-termination
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, request-termination, status-code, echo, plugins, maintenance]
level: intro
status: docs-checked
description: "request-termination plugin: status_code default 503 (100-599), message, raw body with content_type, echo for debugging, trigger header, and invalid combinations."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong/plugins/request-termination/schema.lua
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# request-termination

Stops a request in Kong and returns a fixed response. HTTP protocols only.

| Field | Default | Notes |
|---|---|---|
| `status_code` | `503` | integer, 100 to 599 |
| `message` | none | text for the default response generator |
| `content_type` | none | content type of the raw `body`; requires `body` |
| `body` | none | raw response body |
| `echo` | `false` | echo a copy of the request back, mainly for debugging |
| `trigger` | none | header name; combine with `echo` to debug live traffic |

Rejected combinations:
- `message` with `content_type` or `body`
- `content_type` without `body`
- `echo` with `content_type` or `body`

So either use `message`, or `body` plus `content_type`, or `echo`.

## Checked

2026-11-04. Confirmed against the request-termination schema.lua: status_code default 503 between 100 and 599, message, content_type, body, echo default false, trigger header name, and the three custom_validator rejections.

Method: documentation only; no commands were run.

