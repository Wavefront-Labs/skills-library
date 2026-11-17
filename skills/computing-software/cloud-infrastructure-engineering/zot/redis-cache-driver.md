---
id: computing-software.cloud-infrastructure-engineering.zot.redis-cache-driver
name: redis-cache-driver
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, redis-cache, key-prefix, redis-sentinel, redis-cluster, remote-cache]
level: advanced
status: docs-checked
description: "Configure Zot's Redis cacheDriver using a url or individual keys, keyprefix sharing rules, cluster URLs, and why Sentinel needs individual keys."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/storage.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Requires `remoteCache: true` and `cacheDriver` with `name: redis`.

```json
"cacheDriver": { "name": "redis", "url": "redis://localhost:6379", "keyprefix": "zot" }
```

- `url`: optional; may carry query parameters and supports single-instance and cluster setups. It is used only if present.
- If `url` is absent, individual keys are read from `cacheDriver`.
- `keyprefix`: default `zot`. Instances sharing a database and storage should use the same prefix; instances with different images should use different prefixes.
- Sentinel is not supported through `url`. Use the individual keys and set `master_name`.

Individual keys include: `addr`, `client_name`, `db`, `protocol`, `username`, `password`, `sentinel_username`, `sentinel_password`, retry settings (`max_retries`, `min_retry_backoff`, `max_retry_backoff`), timeouts (`dial_timeout`, `read_timeout`, `write_timeout`), pool settings (`pool_size`, `pool_timeout`, `min_idle_conns`, `max_idle_conns`, `max_active_conns`, `conn_max_idle_time`, `conn_max_lifetime`), `max_redirects`, `read_only`, `route_by_latency`, `route_randomly`, `master_name`, and others.

Warning: do not set every parameter together. Some are mutually exclusive across single-instance, cluster and Sentinel setups.

## Checked

2026-11-04. Read against the zot storage planning article (Redis cache driver section); every remaining claim found there. Removed: nothing.

Method: documentation only; no commands were run.
