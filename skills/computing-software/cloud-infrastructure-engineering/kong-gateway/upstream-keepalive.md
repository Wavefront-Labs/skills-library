---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.upstream-keepalive
name: upstream-keepalive
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, upstream-keepalive-pool-size, keepalive-idle-timeout, keepalive-max-requests, kong-conf, performance]
level: advanced
status: docs-checked
description: "Tune Kong's keep-alive connections to upstreams: upstream_keepalive_pool_size 512, max_requests 10000, idle_timeout 60, and client-side keepalive_requests."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong.conf.default
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upstream keepalive

| Setting | Default | Meaning |
|---|---|---|
| `upstream_keepalive_pool_size` | `512` | default size of upstream keep-alive pools, segmented by dst ip/dst port/SNI; `0` disables upstream keep-alive |
| `upstream_keepalive_max_requests` | `10000` | default max requests proxied through one keep-alive connection; `0` means no limit |
| `upstream_keepalive_idle_timeout` | `60` | seconds an unused upstream keep-alive connection is kept open; `0` means it may stay open indefinitely |

Client-facing keep-alive is separate: `nginx_http_keepalive_requests` (default `10000`) is the maximum number of client requests served through one keep-alive connection. Too high a value could cause excessive memory usage.

Limits that interact:
- `nginx_main_worker_rlimit_nofile` and `nginx_events_worker_connections` default to `auto`, derived from `ulimit -n` and capped at 16384.
- `auto` has a lower bound of 1024.

## Checked

2026-11-04. Confirmed against kong.conf.default: the three upstream defaults and zero-value meanings, `nginx_http_keepalive_requests`, and the `auto` rules for `nginx_main_worker_rlimit_nofile` and `nginx_events_worker_connections`. Removed the Service timeout line, which this source does not state.
Method: documentation only; no commands were run.
