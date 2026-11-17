---
id: computing-software.cloud-infrastructure-engineering.thanos.receive-limits-and-gates
name: receive-limits-and-gates
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-receive, request-limits, gates, limits-config]
level: sme
status: docs-checked
description: "Apply experimental per-tenant request size, series and sample limits and concurrency gates to Thanos Receive."
sources: ["https://thanos.io/tip/components/receive.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Receive limits and gates

Experimental. Limits reject with an error; gates make a request wait for capacity. Everything is disabled by default. Load a YAML file with `--receive.limits-config-file` (reloaded on change; an invalid update is logged and ignored) or inline with `--receive.limits-config`.

```yaml
write:
  global:
    max_concurrency: 30
    meta_monitoring_url: "http://localhost:9090"
    meta_monitoring_limit_query: "sum(prometheus_tsdb_head_series) by (tenant)"
  default:
    request:
      size_bytes_limit: 1024
      series_limit: 1000
      samples_limit: 10
    head_series_limit: 1000
  tenants:
    acme:
      request: { size_bytes_limit: 0 }
      head_series_limit: 2000
```

Rules: `0` means no limit; missing values in `default` or `global` mean no limit; missing values under `tenants` inherit the default.

**Request limits** (per request): `size_bytes_limit`, `series_limit`, `samples_limit`. Exceeding gives HTTP 413, which clients such as Prometheus do not retry in smaller pieces, so data is lost; monitor these.

**Active series limiting** uses a Prometheus-compatible meta-monitoring endpoint, queried every 15 seconds. It is best-effort: if meta-monitoring is unreachable, limits are not enforced.

`max_concurrency` is a gate covering HTTP, OTLP and Cap'n Proto writes.

## Checked

2026-11-03. Confirmed against the Thanos Receive page (components/receive.md) and the Thanos troubleshooting page (operating/troubleshooting.md): hashrings and ketama, shuffle sharding, tenancy and decommissioning, quorum formula, Cap'n Proto, limits and gates, defaults, out-of-bound and out-of-order causes. Added the documented fixes and the out-of-order window flag warnings. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
