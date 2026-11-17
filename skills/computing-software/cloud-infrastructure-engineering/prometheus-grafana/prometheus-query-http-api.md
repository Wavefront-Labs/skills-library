---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-query-http-api
name: prometheus-query-http-api
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, query-api, query-range-api, step-alignment, http-api, curl, jq, automation]
level: practitioner
status: verified
description: "Script against Prometheus /api/v1/query and query_range: parameters, step alignment and the 11,000-point limit, result types, metadata endpoints, and error handling."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Query and query_range HTTP APIs

## Instant query
```bash
curl -sG http://prom:9090/api/v1/query \
  --data-urlencode 'query=sum by (job) (rate(http_requests_total[5m]))' \
  --data-urlencode 'time=2026-10-16T00:00:00Z'
```
The answer is JSON; read `.data.result[]`, each `{metric, value:[ts,"str"]}`. A POST with a form body worked the same (run). A `time` outside retention returns an empty vector, not an error (run).
`resultType`: `vector` (list of `{metric, value:[ts,"str"]}`), `scalar`, `string`, or `matrix` (when the
query is a range selector like `up[5m]`, returning raw samples).

## Range query
```bash
curl -sG http://prom:9090/api/v1/query_range \
  --data-urlencode 'query=rate(node_cpu_seconds_total{mode="idle"}[5m])' \
  --data-urlencode start=2026-10-15T00:00:00Z --data-urlencode end=2026-10-16T00:00:00Z \
  --data-urlencode step=60s
```
- Points = (end - start) / step; max **11,000** per series, else HTTP 400 `exceeded maximum resolution of 11,000 points per timeseries. Try decreasing the query resolution (?step=XX)` (run: a 5 h range at `step=1s` failed, at `step=2s` succeeded).
- Evaluates the expression independently at start, start+step, ...: it is NOT raw data. Use a range
  selector with `/query` to get raw samples.
- **Step alignment**: results are evaluated at start, start+step, ...; rounding `start` down to a multiple of step in scripts (`start = floor(start/step)*step`) makes repeated runs return the same sample timestamps. 
- Choose `[range] >= step` in `rate()` or samples between steps are skipped.

## Other useful endpoints
| Endpoint | Use |
|---|---|
| `/api/v1/series?match[]=...&start=&end=` | which series exist |
| `/api/v1/labels`, `/api/v1/label/<name>/values?match[]=` | label discovery (bound with match[] and time range) |
| `/api/v1/metadata?metric=` | type/help/unit (metadata scraped from targets only; `up` is generated and returned `{}`, run) |
| `/api/v1/query_exemplars` | exemplars for a query and range |
| `/api/v1/format_query?query=` | pretty-print PromQL |
| `/api/v1/parse_query?query=` | AST as JSON (ran on 3.15.1) |
All accept POST with `application/x-www-form-urlencoded` for long queries (avoid URL length limits).

## Errors and limits
`status: "error"`, `errorType` (from `web/api/v1/api.go` at v3.15.1: `bad_data` 400, `execution` 422, `timeout` 503, `canceled` 499, `internal` 500, `not_found` 404, `not_acceptable` 406, `unavailable`; `bad_data` was seen here for a parse error and for the 11,000-point limit). The API docs describe 400 for bad parameters, 422 for an expression that cannot be executed and 503 for timeouts or aborts.
`warnings` / `infos` arrays carry non-fatal notes: `rate(up[1m])` returned `infos: PromQL info: metric might not be a counter, name does not end in _total/_sum/_count/_bucket`, and `histogram_quantile(0.5, up)` returned a `warnings` entry about the missing `le` label. Optional `timeout=` and `limit=` (max returned series; `limit=1` returned one series plus `warnings: ["results truncated due to limit"]`, run) parameters.

## Verify
- [ ] Script checks `.status == "success"` and surfaces `.warnings`.
- [ ] Range queries keep points per series under 11,000 and use aligned starts.

## Checked
Prometheus 3.15.1 (windows-amd64) run locally: instant query (GET, POST form, RFC 3339 and past `time`), range query at the 11,000-point boundary, `stats=all`, `format_query`, `parse_query`, `limit=`, metadata and exemplars endpoints (empty), parse error 400 body, `infos` and `warnings` examples. Docs read: querying/api.md at tag v3.15.1 (status codes, limit).
