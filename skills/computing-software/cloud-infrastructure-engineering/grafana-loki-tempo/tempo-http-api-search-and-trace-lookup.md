---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.tempo-http-api-search-and-trace-lookup
name: tempo-http-api-search-and-trace-lookup
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [tempo-http-api, tempo, trace-by-id, search-api, search-tags, tag-values, tempo-api]
level: practitioner
status: docs-checked
description: "Query Tempo over HTTP by trace ID, TraceQL search and tag discovery, with start/end bounds, tenant header and the TraceQL metrics endpoints."
sources: ["https://grafana.com/docs/tempo/latest/api_docs/", "https://grafana.com/docs/tempo/latest/configuration/tenant-ids/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: scripted trace lookup and discovery. All query endpoints are on the query-frontend (or the single Tempo process in monolithic mode). When multi-tenancy is enabled every request must carry `X-Scope-OrgID`.

```
# one trace (optional start/end in unix epoch seconds)
curl -s -H 'Accept: application/json' -H 'X-Scope-OrgID: <TENANT>' \
  'http://tempo:3200/api/traces/<TRACE_ID>?start=<START>&end=<END>'

# TraceQL search
curl -G -s http://tempo:3200/api/search \
  --data-urlencode 'q={ status=error }' --data-urlencode 'limit=20' \
  --data-urlencode 'start=<START>' --data-urlencode 'end=<END>'

# tag discovery
curl -s 'http://tempo:3200/api/v2/search/tags?scope=span'
curl -s 'http://tempo:3200/api/v2/search/tag/.service.name/values'
```
Endpoints: `GET /api/traces/<id>`, `GET /api/v2/traces/<id>` (V2 adds experimental span pruning and a `q` filter), `GET /api/search` (`q` for TraceQL; `tags` logfmt, `minDuration`, `maxDuration` for tag search; `limit` default 20, `spss` default 3), `GET /api/search/tags`, `GET /api/v2/search/tags` (`scope` = `resource|span|intrinsic|event|link|instrumentation`), `GET /api/search/tag/<tag>/values`, `GET /api/v2/search/tag/<tag>/values` (values with types, optional filtering `q` with a single `{}` selector), `GET /api/metrics/query_range` and `GET /api/metrics/query` (TraceQL metrics: `q`, `start`, `end`, `since` default 1h, `step`, `exemplars`), `GET /api/echo`, `GET /ready`, `GET /metrics`, `GET /api/status/buildinfo`, `/api/overrides`.

Output: JSON by default (OpenTelemetry-style trace); `Accept: application/protobuf` returns OpenTelemetry proto.

Gotchas
- Trace by ID without `start`/`end` checks all backend blocks; with them it only checks blocks in that range, so a trace outside the range can be missed or partial.
- Search without `start`/`end` searches only recent data in the live store; with both it searches the backend as well.
- Search is a massively parallel search taking the first N results, so identical searches can differ.
- Search responses hold span-set summaries, not whole traces; fetch the trace by ID afterwards.
- Tag lookups without `start`/`end` only fetch recent data from the live store.

## Verify
`GET /api/echo` returns status 200 with body `echo` when the query-frontend is ready; the `metrics` object in search responses reports blocks and bytes inspected.

## Checked
2026-11-03. Confirmed against the Tempo HTTP API page (endpoint table, parameters, defaults, return formats) and the tenant IDs page (`X-Scope-OrgID`). Removed: `max_bytes_per_trace` truncation claim for search, the "empty results without tenant header" wording, the "compact protobuf" description, and the `date -d` time arithmetic.
Method: documentation only; no commands were run.
