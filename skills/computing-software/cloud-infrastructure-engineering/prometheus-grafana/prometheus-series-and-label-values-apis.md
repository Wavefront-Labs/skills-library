---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-series-and-label-values-apis
name: prometheus-series-and-label-values-apis
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus-series-api, label-values-api, query-api, grafana-variables, cardinality-analysis, prometheus]
level: practitioner
status: gated
description: "Use /api/v1/series, /api/v1/labels and label values endpoints with match[], time bounds and limits for exploration, Grafana variables and cardinality checks."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/api/#finding-series-by-label-matchers", "https://prometheus.io/docs/prometheus/latest/querying/api/#getting-label-names", "https://grafana.com/docs/grafana/latest/datasources/prometheus/template-variables/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Series, labels and label values APIs

## Endpoints
```bash
# series matching selectors (returns label sets, no values); at least one match[] is required
curl -sG localhost:9090/api/v1/series --data-urlencode 'match[]=up{job="node"}' \
  --data-urlencode "start=$(date -d '-1h' +%s)" --data-urlencode "end=$(date +%s)"
# all label names (optionally restricted by match[])
curl -sG localhost:9090/api/v1/labels --data-urlencode 'match[]=http_requests_total'
# values of one label
curl -sG localhost:9090/api/v1/label/job/values
curl -sG localhost:9090/api/v1/label/route/values --data-urlencode 'match[]=http_requests_total{job="api"}'
```
`limit=<n>` caps results (3.15.1: `limit=1` returned one item plus the warning `results truncated due to limit`, for series and label values). POST with form encoding for long selectors (ran on `/series`). `/api/v1/series` without any `match[]` returns 400 `no match[] parameter provided`.

## Uses
- Grafana variables: `label_values(http_requests_total{job="$job"}, route)` calls the label values endpoint with `match[]`; `query_result(...)` runs an instant query instead (slower).
- Cardinality: count of series for a metric, or distinct values per label, without running a heavy PromQL `count`.
- Discovery of what a target exposes.

## Performance
- `start` and `end` are optional here; the docs call them approximate (a result can include series with no samples in the window) and do not state a default range for these endpoints, so always pass a time range on big servers.
- `match[]={__name__=~".+"}` on `/api/v1/series` is as expensive as it sounds.
- Thanos/Mimir support the same endpoints, often with extra limits such as `max_fetched_series_per_query` (gated: unconfirmed, source is paywalled or blocked; not run here).

## Gotchas
- Label names with special characters can be written in the path with the `U__` escaping (docs example `/api/v1/label/U__http_2e_status_code/values`); the docs say the escaping is optional and is needed when the name contains `/`. The escaping rules: letters, digits and colons as-is, `_` becomes `__`, other characters become `_<hex codepoint>_`. Not run here (no UTF-8 label in the test data).
- The series endpoint can include stale-but-in-range series. Run: after `delete_series` (admin API) a series still came back from `/api/v1/series` immediately while an instant query on it was empty.

## Verify
- [ ] Grafana variable queries specify `match[]` and complete in under a second.

## Checked
Prometheus 3.15.1 (windows-amd64) run locally with the admin API on: `/api/v1/series` (GET, POST, no match[] error, `limit`), `/api/v1/labels` with `match[]`, `/api/v1/label/job/values` with and without `limit`, and a delete_series then series check using a pushed metric. Docs read: querying/api.md at tag v3.15.1 (limit, approximate start/end, `U__` escaping section). Not run: UTF-8 label values, Grafana variable query timing, Thanos/Mimir.
