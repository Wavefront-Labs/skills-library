---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.rate-limiting-policy
name: rate-limiting-policy
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, rate-limiting-policy, redis-policy, sync-rate, fault-tolerant, plugins]
level: advanced
status: docs-checked
description: "rate-limiting policy choices local, cluster and redis, fault_tolerant default true, sync_rate -1 versus 0.02 minimum, required redis fields, and DB-less restrictions."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong/plugins/rate-limiting/schema.lua
  - https://developer.konghq.com/gateway/hybrid-mode/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rate-limiting policy and sync

`policy` (default `local`):
- `local`: in-memory counters per node
- `cluster`: counters in the Kong data store
- `redis`: counters in a Redis server

In DB-less mode (`database=off`) or on a control plane only `local` and `redis` are allowed. In hybrid mode the `cluster` strategy is unsupported.

`policy: redis` requires `redis.host`, `redis.port` and `redis.timeout`. Redis fields go under `config.redis`; the older flat `redis_host`, `redis_port` and friends are deprecated and removed in Kong 4.0.

`sync_rate` (default `-1`): `-1` means synchronous counting. Any other value is allowed only with `policy: redis`, and must be at least `0.02`.

`fault_tolerant` (default `true`): keep proxying if the data store is unreachable.

Example:

```yaml
config:
  policy: redis
  redis:
    host: <REDIS_HOST>
    port: 6379
```

The newer docs also describe `redis.username` and cloud authentication providers for managed Redis.

Window and key options are in the rate-limiting limits skill.

## Checked

2026-11-04. Confirmed against the rate-limiting schema.lua (policy values and DB-less/control plane restriction, sync_rate -1 and 0.02 checks, fault_tolerant default true, required redis host/port/timeout, deprecated flat redis fields removed in 4.0) and the hybrid mode and plugin pages (cluster policy unsupported in hybrid mode, redis.username and cloud authentication).

Method: documentation only; no commands were run.
