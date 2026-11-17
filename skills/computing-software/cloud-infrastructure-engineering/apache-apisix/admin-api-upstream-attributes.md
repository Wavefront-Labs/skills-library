---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.admin-api-upstream-attributes
name: admin-api-upstream-attributes
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, admin-api, upstream, load-balancing, chash, pass-host, retries]
level: practitioner
status: docs-checked
description: "Upstream object attributes in the APISIX Admin API: balancer type, nodes and priority, hash_on and key, retries, timeout, scheme and pass_host."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/admin-api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upstream attributes

- `type`: `roundrobin` (default), `chash`, `ewma`, `least_conn`, or a custom balancer.
- `nodes`: map or array of addresses with weights; or `service_name` plus `discovery_type` for service discovery. A node can carry `priority` (default 0); negative priority acts as a backup.
- `hash_on` (with `chash`): `vars` (default), `header`, `cookie`, `consumer`, `vars_combinations`. `key` is required for all but `consumer`.
- `checks`: health check configuration.
- `retries`: set according to the number of available backend nodes by default; 0 disables retries. `retry_timeout`: 0 disables it.
- `timeout`: `connect`, `send`, `read` in seconds.
- `scheme`: `http` default; also `https`, `grpc`, `grpcs`, `ws`, `wss`, `tcp`, `udp`, `tls`.
- `pass_host`: `pass` (default), `node`, or `rewrite`. `upstream_host` applies only with `rewrite`.
- `tls.*`, `keepalive_pool.*`, `warm_up_conf.*`: optional TLS, connection pool and slow-start settings.

## Checked

2026-11-04: read the Admin API page (Upstream table, type list and hash_on notes, node priority section). Confirmed type values, nodes/priority, hash_on values and key rules, retries and retry_timeout, timeout, scheme values, pass_host and upstream_host, tls, keepalive_pool and warm_up_conf keys. Reworded the retries default to the page's wording.

Method: documentation only; no commands were run.
