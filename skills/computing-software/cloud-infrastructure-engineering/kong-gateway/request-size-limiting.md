---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.request-size-limiting
name: request-size-limiting
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, request-size-limiting, payload-size, require-content-length, plugins, limits]
level: intro
status: docs-checked
description: "request-size-limiting plugin: allowed_payload_size default 128, size_unit bytes, kilobytes or megabytes (default megabytes), and require_content_length."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong/plugins/request-size-limiting/schema.lua
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# request-size-limiting

| Field | Default | Notes |
|---|---|---|
| `allowed_payload_size` | `128` | maximum request payload, in `size_unit` |
| `size_unit` | `megabytes` | `bytes`, `kilobytes` or `megabytes` |
| `require_content_length` | `false` | when `true`, the request must carry a valid `Content-Length` header before the body is read |

So by default the limit is 128 MB.

`size_unit` needs Kong Gateway 1.3+ or open-source 2.0+.

## Checked

2026-11-04. Confirmed against the request-size-limiting schema.lua: allowed_payload_size default 128 (megabytes, 128000000 bytes), size_unit bytes/kilobytes/megabytes default megabytes with the 1.3 and OSS 2.0 note, require_content_length default false. Removed the nginx_http_client_max_body_size and nginx_admin_client_max_body_size paragraph: the cited schema does not state those settings or defaults.

Method: documentation only; no commands were run.
