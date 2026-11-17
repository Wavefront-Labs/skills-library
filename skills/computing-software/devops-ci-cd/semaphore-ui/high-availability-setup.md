---
id: computing-software.devops-ci-cd.semaphore-ui.high-availability-setup
name: high-availability-setup
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [high-availability, ha, redis, enterprise, active-active, semaphore-ui]
level: advanced
status: docs-checked
description: "Configure active-active Semaphore HA (Enterprise) with a shared Postgres or MySQL database, Redis and unique node IDs."
sources:
  - https://semaphoreui.com/docs/admin-guide/ha
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# High availability (Enterprise)

Goal: run several Semaphore nodes behind a load balancer.

Components: a load balancer (HTTP and WebSocket), identical Semaphore nodes, a shared PostgreSQL or MySQL database, and Redis for distributed locks, the shared task queue and pub/sub events. SQLite and BoltDB are not supported; Redis Cluster is not supported (single Redis or Sentinel). An Enterprise subscription key is required.

Every node uses the same database, Redis and configuration, except a unique `ha.node_id`.

```json
{
  "dialect": "postgres",
  "postgres": { "host": "db.example.com:5432", "name": "semaphore", "user": "semaphore", "pass": "***" },
  "ha": {
    "enabled": true,
    "node_id": "node-1",
    "redis": { "addr": "redis.example.com:6379", "db": 0, "pass": "***" }
  },
  "cookie_hash": "...",
  "cookie_encryption": "...",
  "access_key_encryption": "..."
}
```

Environment form: `SEMAPHORE_HA_ENABLED=true`, `SEMAPHORE_HA_NODE_ID=node-1`, `SEMAPHORE_HA_REDIS_ADDR`, `SEMAPHORE_HA_REDIS_DB`, `SEMAPHORE_HA_REDIS_PASS`. Also `ha.redis.user`, `ha.redis.tls`, `ha.redis.tls_skip_verify`.

Gotchas:
- `cookie_hash`, `cookie_encryption` and `access_key_encryption` must be identical on all nodes.
- Redis provides the locks that stop two nodes running the same job.

Verify: a task started via one node shows live in the UI of another, and stopping one node leaves the service up.

## Checked

2026-11-04: checked against the high availability page. Every claim is stated there.

Method: documentation only; no commands were run.
