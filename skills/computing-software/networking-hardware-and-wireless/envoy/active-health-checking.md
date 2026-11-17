---
id: computing-software.networking-hardware-and-wireless.envoy.active-health-checking
name: active-health-checking
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, health-check, active-health-checking, http-health-check, grpc-health-check, tcp-health-check, redis, eds]
level: practitioner
status: docs-checked
description: "Choose HTTP, gRPC, L3/L4 or Redis active health checks per Envoy cluster and know how a failed check affects traffic."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/upstream/health_checking.rst
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/configuration/upstream/cluster_manager/cluster_hc.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# active health checking
Active health checking is configured per upstream cluster and pairs naturally with EDS, but it also helps for other discovery types. Checker types:
- HTTP: sends an HTTP request and by default expects 200; expected and retriable status codes are configurable. A non-expected or non-retriable code (any non-200 by default) lets the host signal it should stop receiving traffic immediately.
- gRPC: sends a gRPC health request, 200 by default.
- L3/L4: sends a configurable byte buffer and expects it echoed back; a connect-only mode is also supported.
- Redis: sends PING and expects PONG; optionally runs EXISTS on a key (`redis_key`), and a missing key counts as a passing check, so setting the key marks the instance for maintenance and traffic drains.
- Thrift: sends a Thrift request and expects a success response.

```yaml
health_checks:
- timeout: 1s
  interval: 5s
  unhealthy_threshold: 3
  healthy_threshold: 2
  http_health_check: { path: /healthz }
```
Gotchas: startup includes a single active health check round before listeners open. Health checks run over the cluster's transport socket, so a TLS cluster is checked over TLS. Passive (outlier detection) and active checks can be combined. `GET /clusters` prints a `healthy` field per host; when unhealthy it contains strings such as `/failed_active_hc`.

## Checked
2026-11-03. Confirmed against health_checking.rst, the admin /clusters entry and the HealthCheck reference. Removed or corrected: the health_status claim, the health_flags field name (the admin page shows a healthy field) and the 'four types' count (Thrift is also listed).
Method: documentation only; no commands were run.
