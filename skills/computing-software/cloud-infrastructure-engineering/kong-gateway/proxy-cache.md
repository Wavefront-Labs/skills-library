---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.proxy-cache
name: proxy-cache
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, proxy-cache, cache-ttl, x-cache-status, plugins, caching]
level: practitioner
status: docs-checked
description: "proxy-cache plugin config: response_code 200/301/404, request_method GET/HEAD, content_type, cache_ttl 300, strategy memory, vary lists and diagnostic headers."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong/plugins/proxy-cache/schema.lua
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# proxy-cache

| Field | Default | Notes |
|---|---|---|
| `response_code` | `200, 301, 404` | each 100 to 900 |
| `request_method` | `GET, HEAD` | any of HEAD, GET, POST, PATCH, PUT |
| `content_type` | `text/plain, application/json` | exact match on upstream content type |
| `cache_ttl` | `300` | seconds, greater than 0 |
| `strategy` | required | storage backend, for example `memory` |
| `cache_control` | `false` | respect RFC 7234 Cache-Control when `true` |
| `ignore_uri_case` | `false` | |
| `storage_ttl` | none | seconds to keep entries in storage, independent of other TTLs |
| `memory.dictionary_name` | `kong_db_cache` | shared dictionary for the memory strategy |
| `vary_query_params` | none | query params in the cache key; unset uses all |
| `vary_headers` | none | headers in the cache key; unset uses none |

Diagnostic response headers, each toggled under `response_headers` and default `true`: `age`, `X-Cache-Status`, `X-Cache-Key`.

With `strategy: memory`, the shared dictionary named in `memory.dictionary_name` must exist in the Nginx configuration or the entity is rejected.

Check a hit or miss by reading `X-Cache-Status` on the response.

## Checked

2026-11-04. Confirmed against the proxy-cache schema.lua: every default and range in the table, exact content-type matching, memory dictionary check, vary_query_params/vary_headers behaviour, response_headers defaults.

Method: documentation only; no commands were run.
