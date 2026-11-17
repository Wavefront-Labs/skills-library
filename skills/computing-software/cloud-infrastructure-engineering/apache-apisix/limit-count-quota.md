---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.limit-count-quota
name: limit-count-quota
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, limit-count, rate-limiting, quota, rejected-code, plugin]
level: practitioner
status: docs-checked
description: "Configure the APISIX limit-count plugin: count and time_window, key, rejected_code, quota response headers, fixed or sliding window, and shared groups."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/limit-count.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# limit-count quota

`limit-count` allows `count` requests per `time_window` seconds per key.

Key attributes and defaults:
- `count`, `time_window`: required together (both > 0) unless `rules` is used.
- `window_type`: `fixed` (default) or `sliding` (sliding needs APISIX 3.18.0+).
- `key_type`: `var` (default), `var_combination`, `constant`; `key` defaults to `remote_addr`.
- `rejected_code`: 503 by default (200-599); `rejected_msg` sets the body.
- `show_limit_quota_header`: true, so responses carry `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`.
- `group`: routes with the same group string share one counter.
- `allow_degradation`: false; when true, requests pass unlimited if the counter backend fails.

```shell
curl "http://127.0.0.1:9180/apisix/admin/routes" -X PUT \
  -H "X-API-KEY: ${admin_key}" \
  -d '{"id":"limit-count-route","uri":"/get",
       "plugins":{"limit-count":{"count":1,"time_window":30,"rejected_code":429,"key":"remote_addr","policy":"local"}},
       "upstream":{"type":"roundrobin","nodes":{"httpbin.org:80":1}}}'
```

A second request inside 30 seconds returns 429.

With `rules`, headers use `X-<prefix>-RateLimit-*`, where the prefix is `header_prefix` or the one-based rule index. A backend failure or an invalid resolved `count` returns 500 unless `allow_degradation` is true.

## Checked

2026-11-04. Confirmed against the APISIX limit-count plugin page: count/time_window requirement, window_type and the 3.18.0 gate for sliding, key_type values, rejected_code default, quota headers and the rules header prefix, group sharing, allow_degradation and the 500 behaviour. Nothing removed.

Method: documentation only; no commands were run.
