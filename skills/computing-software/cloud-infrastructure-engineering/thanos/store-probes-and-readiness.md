---
id: computing-software.cloud-infrastructure-engineering.thanos.store-probes-and-readiness
name: store-probes-and-readiness
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-store, readiness-probe, healthy, ready]
level: intro
status: docs-checked
description: "Use the /-/healthy and /-/ready endpoints of Thanos Store for Kubernetes probes."
sources: ["https://thanos.io/tip/components/store.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Store probes

Thanos Store exposes two probe endpoints on its HTTP port (default `0.0.0.0:10902`):

- `/-/healthy` becomes healthy as soon as initial setup completes.
- `/-/ready` becomes ready only after all bootstrapping, such as the initial index building, has finished and the store can serve traffic.

The metrics endpoint starts immediately, so a readiness probe must point at `/-/ready` rather than `/metrics`, otherwise traffic can arrive before the store is usable.

```yaml
readinessProbe:
  httpGet:
    path: /-/ready
    port: 10902
livenessProbe:
  httpGet:
    path: /-/healthy
    port: 10902
```

`thanos tools bucket downsample` (the downsample service) exposes `/-/healthy` with the same meaning.

Related shutdown flags: `--http-grace-period` and `--grpc-grace-period` both default to 2m, the time to wait after an interrupt.

## Checked

2026-11-03. Confirmed against the Thanos Store page (components/store.md): disk sizing (6 MB, 30MB), probes, index cache types and config, memcached and redis options, circuit breaker, caching bucket options, groupcache (v0.25, /_groupcache warning), hedging defaults, request limits and deprecations, time partitioning. Removed the claim about raw Prometheus blocks in the data dir. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
