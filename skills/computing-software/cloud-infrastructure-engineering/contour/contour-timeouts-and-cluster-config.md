---
id: computing-software.cloud-infrastructure-engineering.contour.contour-timeouts-and-cluster-config
name: contour-timeouts-and-cluster-config
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [timeouts, request-timeout, idle-timeout, connect-timeout, circuit-breakers, max-requests-per-connection, dns-lookup-family, buffer-limit]
level: practitioner
status: docs-checked
description: "Contour config timeouts and cluster blocks: request, idle, connection, connect timeouts with defaults, circuit breaker defaults, dns-lookup-family, per-connection buffer limits."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/configuration.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Contour timeouts and cluster config blocks

`timeouts` (all optional; values are Go durations, or `infinity` where noted):
- `request-timeout`: whole-request timeout; omit or `infinity` disables. `0s` no longer disables it.
- `connection-idle-timeout`: `60s`.
- `stream-idle-timeout`: `5m` (Envoy default); `infinity` disables.
- `max-connection-duration`: none by default.
- `delayed-close-timeout`: `1s`, an advanced setting.
- `connection-shutdown-grace-period`: `5s` between the first and final HTTP/2 GOAWAY.
- `connect-timeout`: `2s` for upstream connection establishment.

`cluster` block:
- `dns-lookup-family`: `auto` (default), `v4`, `v6`, `all` for ExternalName upstreams.
- `max-requests-per-connection`: no limit by default; `1` effectively disables keep-alive.
- `per-connection-buffer-limit-bytes`: soft limit, Envoy default 1MiB.
- `circuit-breakers`: global defaults used when the per-service annotations are absent: `max-connections` (1024), `max-pending-requests` (1024), `max-requests` (1024), `max-retries` (3). 0 means use the default.

```yaml
timeouts:
  request-timeout: 30s
  stream-idle-timeout: 5m
cluster:
  max-requests-per-connection: 0
  circuit-breakers:
    max-connections: 2048
```

`network` block: `num-trusted-hops` (0) extra x-forwarded-for hops to trust; `admin-port` (9001, `0` disables the Envoy admin listener); `strip-trailing-host-dot` (false).

## Checked

2026-11-04. Confirmed against the Contour Configuration Reference (configuration.md): the fields, defaults, flags and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
