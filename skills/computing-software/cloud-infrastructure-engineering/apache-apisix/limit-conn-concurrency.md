---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.limit-conn-concurrency
name: limit-conn-concurrency
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, limit-conn, concurrency, burst, rate-limiting, plugin]
level: practitioner
status: docs-checked
description: "Cap concurrent requests in APISIX with limit-conn: conn, burst, default_conn_delay, only_use_default_delay, key, key_ttl and Redis policies."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/limit-conn.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# limit-conn concurrency

Counts concurrent requests per `key` (default `remote_addr`).

Attributes:
- `conn` and `burst`: integer or lua-resty-expr; required unless `rules` is set (`rules` needs APISIX 3.16.0+).
- `default_conn_delay`: required, > 0.
- `only_use_default_delay`: false by default.
- `key_type`: `var` (default) or `var_combination`.
- `rejected_code` 503 by default; `rejected_msg` optional.
- `policy`: `local` (default), `redis`, `redis-cluster`; `key_ttl` 3600 seconds for shared counters.

Zones:
- Up to `conn`: served at once.
- Between `conn` and `conn + burst`: delayed. The delay grows with how far the request exceeds `conn`, or is always `default_conn_delay` when `only_use_default_delay` is true. Example with conn 5, burst 3, delay 1: the 6th, 7th, 8th requests wait 1, 2, 3 seconds.
- Beyond `conn + burst`: rejected immediately.

```shell
curl "http://127.0.0.1:9180/apisix/admin/routes/limit-conn-min" -X PUT \
  -H "X-API-KEY: ${admin_key}" \
  -d '{"uri":"/get","plugins":{"limit-conn":{"conn":2,"burst":1,"default_conn_delay":0.1}},"upstream":{"type":"roundrobin","nodes":{"httpbin.org:80":1}}}'
```

With `allow_degradation` true, requests bypass the plugin if its backing store is unavailable.

## Checked

2026-11-04. Confirmed against the APISIX limit-conn plugin page: attribute defaults and requirements, the conn/burst/delay zones and the 1, 2, 3 second example, key_ttl 3600, policy values, rules from 3.16.0, allow_degradation. Nothing removed.

Method: documentation only; no commands were run.
