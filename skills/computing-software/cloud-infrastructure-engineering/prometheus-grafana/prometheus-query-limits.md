---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-query-limits
name: prometheus-query-limits
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, query-max-samples, query-timeout-tuning, query-max-concurrency, lookback-delta, oom-protection]
level: practitioner
status: verified
description: "Protect Prometheus from expensive queries with --query.max-samples, --query.timeout and --query.max-concurrency: sizing, error messages users see, and safe values."
sources: ["https://prometheus.io/docs/prometheus/latest/command-line/prometheus/", "https://prometheus.io/docs/prometheus/latest/querying/api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Query limits

| Flag | Default | Effect when hit |
|---|---|---|
| `--query.max-samples` | 50000000 | Query fails: `query processing would load too many samples into memory in query execution` |
| `--query.timeout` | 2m | `query timed out in expression evaluation` (HTTP 503) |
| `--query.max-concurrency` | 20 | Maximum number of queries executed concurrently; the rest wait |
| `--query.lookback-delta` | 5m | Not a limit; how far back an instant selector looks for a sample |

## Sizing max-samples
The flag caps the samples a single query may load into memory (3.15.1 returned HTTP 422 with `query processing would load
too many samples into memory in query execution` for a query over the limit). Memory per sample is not documented: measure
`process_resident_memory_bytes` while running a query near the limit, then pick `max-samples x max-concurrency` that fits.
Lower it on small instances; the error tells the user to narrow the query rather than OOM-killing everyone's dashboards.

## Timeout and concurrency
- Grafana's Prometheus data source has its own "Query timeout" setting (default 60s in the Grafana docs); set Prometheus' a bit
  higher so you see the Prometheus error, not a generic proxy timeout.
- Watch `prometheus_rule_group_last_duration_seconds` while dashboards are busy: rule groups and queries compete for the same server.
- Per-request override: the HTTP API accepts `timeout=`; it can only lower the server limit (with `--query.timeout=300ms`, a
  request with `timeout=50s` still returned `503 query timed out in expression evaluation`).

## Remote/long-range stores
For Thanos/Mimir the equivalent limits are per component: Mimir `max_fetched_series_per_query`,
`max_fetched_chunk_bytes_per_query`, `max_query_lookback` (Mimir configuration reference); Thanos Query `--query.max-concurrent`
(default 20) and Store Gateway `--store.grpc.series-sample-limit` (Thanos component docs). Neither was run here.

## Verify
- [ ] `curl /api/v1/status/flags | jq '.data["query.max-samples"]'` shows the new value.
- [ ] A deliberately huge query fails fast with the max-samples error instead of OOM.
- [ ] `prometheus_engine_queries_concurrent_max` and queue time stay in bounds at peak.

## Checked
Environment: Windows 11, Prometheus and promtool 3.15.1 (windows-amd64), client_golang 1.25.0 on Go 1.26.
- Servers started with `--query.max-samples=200` and `--query.timeout=3s`: `/api/v1/status/flags` returned the four `query.*` values; a query over the sample limit returned HTTP 422 with the message above; `prometheus_engine_queries_concurrent_max` was 20. A server with `--query.timeout=300ms`: a subquery taking about 0.7 s returned `503 query timed out in expression evaluation`, with and without `timeout=50s` on the request; with the default limit the same query succeeded.
- Defaults (50000000, 2m, 20, 5m) from `prometheus --help`; `jq '.data["query.max-samples"]'` ran under jq 1.8.2 (returned "50000000").
- Mimir names: Mimir configuration reference (`limits` block). Thanos flags: Thanos query and store component docs. Grafana's default query timeout: Grafana Prometheus data-source configuration page.
