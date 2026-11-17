---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.loki-http-api-push-and-query
name: loki-http-api-push-and-query
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [loki-http-api, loki, push-api, query-range-api, loki-api, json-push, snappy-protobuf]
level: practitioner
status: docs-checked
description: "Use the Loki HTTP API to push JSON logs and run instant, range and label queries with curl."
sources: ["https://grafana.com/docs/loki/latest/reference/loki-http-api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: scripts and health checks that write and read Loki directly.

Push. The default body is Snappy-compressed protobuf (`Content-Type: application/x-protobuf`); with `Content-Type: application/json` you can send JSON:
```
curl -X POST http://loki:3100/loki/api/v1/push \
  -H 'Content-Type: application/json' -H 'X-Scope-OrgID: team-a' \
  --data-raw '{"streams":[{"stream":{"app":"demo","env":"test"},"values":[["'"$(date +%s)000000000"'","hello from curl"]]}]}'
```
Timestamps are nanosecond Unix epochs sent as strings; a number instead of a string returns 400. A value may carry a third element: a flat JSON object of string keys and string values (structured metadata) placed right after the log line.

Query range:
```
curl -G -s http://loki:3100/loki/api/v1/query_range -H 'X-Scope-OrgID: team-a' \
  --data-urlencode 'query={app="demo"}' --data-urlencode 'limit=10' \
  --data-urlencode "since=10m"
```
`query_range` parameters: `query`, `limit` (default 100, log queries only), `start` (default one hour ago) and `end` (default now) as nanosecond Unix epochs or another supported format, `since` (a duration; `start` supersedes it), `step` (metric queries), `interval` (log queries), `direction` (`forward` or `backward`, default `backward`).

Other endpoints: `/loki/api/v1/query` (instant, metric queries only: a log query returns 400), `/loki/api/v1/labels`, `/loki/api/v1/label/<name>/values`, `/loki/api/v1/series`, `/loki/api/v1/tail`, `/loki/api/v1/index/stats`, `/ready`, `/metrics`, `/config`.

Gotchas
- The response `resultType` follows the query: `streams` for log queries, `matrix` (range) or `vector` (instant) for metric queries.
- `/ready` returns HTTP 200 when the instance accepts traffic; in microservices mode every component exposes it.

## Verify
After the push, `query_range` returns the entry; `curl http://loki:3100/ready` returns HTTP 200.

## Checked
2026-11-03. Confirmed against the Loki HTTP API reference (push formats, string timestamps and 400, structured metadata element, query_range parameters and defaults, instant query 400, resultType values, endpoint list, /ready). Removed: the `start`/`end` shell date arithmetic (replaced by `since`), RFC3339-only claim, the 204-on-push and old-sample 400 claims (not stated on the page), and "HTTP 204" in Verify.
Method: documentation only; no commands were run.
