---
id: computing-software.devops-ci-cd.semaphore-ui.ha-redis-sentinel-and-load-balancer
name: ha-redis-sentinel-and-load-balancer
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [ha, redis-sentinel, load-balancer, nginx, failover, semaphore-ui]
level: advanced
status: docs-checked
description: "Survive Redis failure with ha.engine redis_sentinel and balance nodes with nginx including the websocket route."
sources:
  - https://semaphoreui.com/docs/admin-guide/ha
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HA with Redis Sentinel and a load balancer

Goal: remove Redis and the front end as single points of failure.

Sentinel configuration:

```json
{
  "ha": {
    "enabled": true,
    "node_id": "node-1",
    "engine": "redis_sentinel",
    "redis_sentinel": {
      "master_name": "mymaster",
      "addrs": ["sentinel-1.example.com:26379", "sentinel-2.example.com:26379", "sentinel-3.example.com:26379"],
      "pass": "***"
    }
  }
}
```

Environment: `SEMAPHORE_HA_ENGINE=redis_sentinel`, `SEMAPHORE_HA_REDIS_SENTINEL_MASTER_NAME`, `SEMAPHORE_HA_REDIS_SENTINEL_ADDRS='["host:26379", ...]'` (JSON array), `..._PASS`, plus `..._SENTINEL_USER`, `..._SENTINEL_PASS`, `..._DB`, `..._USER`, `..._TLS`, `..._TLS_SKIP_VERIFY`. `ha.engine` is `redis` (default) or `redis_sentinel`.

Nodes follow a failover without restart; a running task keeps running.

Load balancer (nginx): define an `upstream semaphore` with each node on port 3000 (`max_fails=3 fail_timeout=10s`), proxy `/` with `proxy_next_upstream` on 5xx, and give `/api/ws` its own location with `proxy_http_version 1.1`, `Upgrade`/`Connection "upgrade"` headers and long `proxy_read_timeout` and `proxy_send_timeout` (1h in the sample) so websockets stay open.

Verify: stop the Redis master and confirm the UI and new tasks keep working after Sentinel promotes a replica.

## Checked

2026-11-04: checked against the high availability page and configuration reference. Every claim is stated there.

Method: documentation only; no commands were run.
