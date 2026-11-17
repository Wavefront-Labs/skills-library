---
id: computing-software.cloud-infrastructure-engineering.thanos.query-frontend-overview
name: query-frontend-overview
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-query-frontend, query-splitting, retry, range-queries]
level: intro
status: docs-checked
description: "Put Query Frontend in front of Queriers for splitting, retries and caching of range queries."
sources: ["https://thanos.io/tip/components/query-frontend.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Query Frontend overview

`thanos query-frontend` is a stateless service in front of Queriers, based on the Cortex Query Frontend. Only range queries (`/api/v1/query_range`) are processed; all other calls pass straight to the downstream.

```
thanos query-frontend \
  --http-address "0.0.0.0:9090" \
  --query-frontend.downstream-url="<thanos-querier>:<querier-http-port>"
```

**Splitting.** `--query-range.split-interval` (default 24h) splits long queries into shorter ones. It protects Queriers from OOM, improves parallelism and load balancing, and must be above 0 when caching is configured.

**Retries.** `--query-range.max-retries-per-request` defaults to 5.

**Other limits.** `--query-range.max-query-length` (0 disables), `--query-range.max-query-parallelism` (default 14), and `--query-range.response-cache-max-freshness` (default 1m, newest results not cached).

**Slow query log.** `--query-frontend.log-queries-longer-than` (0 disabled, below 0 logs all). `--query-frontend.slow-query-logs-user-header` sets `remote_user` from a header such as `X-Grafana-User`.

## Checked

2026-11-03. Confirmed against the Thanos Query Frontend page (components/query-frontend.md): splitting, retries, limits and defaults, cache behaviour and exclusions, downstream tripper advice (max_idle_conns_per_host 100; 10 - 20% latency), forward-header, sharding flags, --cache-compression-type. Fixed: cache backends wording. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
