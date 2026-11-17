---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.dynamic-log-level
name: dynamic-log-level
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, dynamic-log-level, debug-node, log-level-api, admin-api, logging]
level: advanced
status: docs-checked
description: "Change Kong's log level at runtime through the Admin API debug endpoints for one node, the cluster, or hybrid data planes, without editing kong.conf."
sources:
  - https://developer.konghq.com/gateway/logs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Changing log level at runtime

Dynamic changes are never written to `kong.conf` and revert when the node restarts.

Endpoints (Admin API):

| Scope | Request |
|---|---|
| Single node | `POST /debug/node/log-level/{logLevel}` |
| Whole cluster | `POST /debug/cluster/log-level/{loglevel}` |
| Control plane nodes | `POST /debug/cluster/control-planes-nodes/log-level/{loglevel}` |
| Data plane nodes (hybrid, v3.16+) | `POST /debug/cluster/data-planes/log-level-operations` |

The data plane operation takes a `log_level`, a target, and an optional `ttl` of 10 to 3600 seconds (default 600).

Example against a local node, using the documented path shape:

```bash
curl -i -X POST http://localhost:8001/debug/node/log-level/debug
```

Valid levels are the same as `log_level`: `debug`, `info`, `notice`, `warn`, `error`, `crit`.

For a permanent change, set `log_level` in `kong.conf` and restart.

## Checked

2026-11-04. Confirmed against the Kong Gateway logs page: the four endpoints, non-persistence, data plane operations (v3.16+, hybrid only), `ttl` 10 to 3600 seconds default 600, and the level names. The page prints the cluster path as `/POST debug/cluster/log-level/{loglevel}`; the skill uses the evident POST form. Nothing removed.
Method: documentation only; no commands were run.
