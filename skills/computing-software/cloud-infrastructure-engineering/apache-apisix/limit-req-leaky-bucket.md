---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.limit-req-leaky-bucket
name: limit-req-leaky-bucket
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, limit-req, leaky-bucket, rate-limiting, burst, nodelay, plugin]
level: practitioner
status: docs-checked
description: "Throttle request rate in APISIX with limit-req: rate, burst, key, nodelay, rejected_code, local versus Redis policy and degradation."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/limit-req.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# limit-req leaky bucket

`limit-req` uses a leaky bucket per key.

Attributes:
- `rate` (required, > 0), `burst` (required, >= 0), `key` (required).
- `key_type`: `var` (default) or `var_combination` (variables each prefixed with `$`).
- `rejected_code`: 503 by default (200-599); `rejected_msg` optional.
- `nodelay`: false by default.
- `allow_degradation`: false by default.
- `policy`: `local` (default), `redis`, `redis-cluster`.

Behavior:
- At or below `rate`: processed immediately.
- Above `rate` but within `burst`: queued and delayed, or processed immediately when `nodelay` is true.
- Above `rate` plus `burst`: rejected with `rejected_code`.

Example, 1 request per second per client address:

```shell
curl "http://127.0.0.1:9180/apisix/admin/routes" -X PUT \
  -H "X-API-KEY: ${admin_key}" \
  -d '{"id":"limit-req-route","uri":"/get","plugins":{"limit-req":{"rate":1,"burst":0,"key":"remote_addr"}},"upstream":{"type":"roundrobin","nodes":{"httpbin.org:80":1}}}'
```

With the `local` policy each gateway instance counts separately, so the cluster-wide limit is about `rate` times the instance count. The `redis` and `redis-cluster` policies share one quota (`redis_host` is required for `redis`).

## Checked

2026-11-04. Confirmed against the APISIX limit-req plugin page: rate, burst and key requirements, key_type, rejected_code, nodelay, allow_degradation and policy defaults, the local-policy per-instance counting, redis_host. Nothing removed.

Method: documentation only; no commands were run.
