---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.logql-performance-and-logcli
name: logql-performance-and-logcli
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [logql, logql-query-performance, query-sharding-loki, logcli-usage, logcli-query, query-stats, bytes-processed]
level: advanced
status: gated
description: "Make LogQL queries fast (selector specificity, filter order, sharding-friendly aggregations, query stats) and use logcli for scripted queries, exports and series inspection."
sources: ["https://grafana.com/docs/loki/latest/query/bp-query/", "https://grafana.com/docs/loki/latest/query/logcli/", "https://grafana.com/docs/loki/latest/operations/query-acceleration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LogQL performance and logcli

## What makes a query expensive
Loki finds streams by label index, then **scans every chunk** of those streams in the time range. Cost ~
bytes in the selected streams x range.
1. **Narrow the stream selector**: use the most specific label (`{app="api"}`); the Loki best-practice page says more general selectors then add nothing.
2. **Line filters first, cheapest first**: `|= "error"` (substring) before `|~` regex before parsers.
   `|= "timeout" | json | status >= 500` is far cheaper than `| json | status >= 500 |= "timeout"`.
3. Parse only what you need: `| json status, path` (named extraction) instead of `| json`.
4. Shorter time ranges; for dashboards use recording rules (ruler) for heavy metric queries.
5. Sharding: query-frontend splits by time (`split_queries_by_interval`, default 1h, confirmed in the config dump) and shards by stream for
   sum/count/rate-style aggregations; `topk`, `quantile_over_time` without `by`, and `sort` limit sharding (gated: unconfirmed, source is paywalled or blocked): a single-binary test node does not run the query-frontend sharding path.
6. Structured metadata lets you filter high-cardinality fields (trace_id) without making them labels (run). Bloom-filter query acceleration for those searches (gated: unconfirmed, source is paywalled or blocked): the bloom components were not run.

## Measure
Grafana Explore -> Query inspector -> Stats: **Total bytes processed**, **Summary: exec time**, chunks
fetched, cache hits. `logcli query --stats` prints the same. Aim to cut bytes processed, not just time.

## logcli
```bash
export LOKI_ADDR=https://loki.example.com LOKI_ORG_ID=tenant-a   # LOKI_USERNAME/LOKI_PASSWORD or LOKI_BEARER_TOKEN
logcli labels namespace
logcli series '{namespace="checkout"}' --analyze-labels      # label cardinality of matching streams
logcli query '{app="api"} |= "error"' --since=1h --limit=500 -o raw
logcli query 'sum by (status) (rate({app="nginx"} | pattern `<_> <status> <_>` [5m]))' --since=6h --step=5m
logcli query '{app="audit"}' --from=2026-10-01T00:00:00Z --to=2026-10-02T00:00:00Z \
  --part-path-prefix=/data/audit --parallel-duration=1h --parallel-max-workers=4 --merge-parts -o jsonl   # bulk export
logcli instant-query 'count_over_time({app="api"}[1h])'
logcli volume '{namespace=~".+"}' --since=24h                 # bytes per stream/label (volume API)
```
`--tail` (`-t`) follows live logs like `tail -f`.

On Windows (logcli 3.7.9) `--merge-parts` failed at the final step with "removing file error ... being used by another process", while the per-hour `.part` files were written correctly; drop `--merge-parts` there and concatenate the parts yourself. Behaviour of the merge on Linux was not run (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] Rewritten dashboard queries show lower "bytes processed" in the inspector.
- [ ] Bulk export via logcli writes one part file per `--parallel-duration` window and the line count across parts matches `count_over_time`.

## Checked
Ran logcli 3.7.9 against a local Loki 3.7.9: `labels`, `series --analyze-labels`, `query --stats`, `query -o jsonl|raw`, `instant-query`, `volume`, `--forward`, `--step`, and the bulk export with `--part-path-prefix`, `--parallel-duration`, `--parallel-max-workers` (120 lines across the part files; `--merge-parts` failed on Windows as noted). `LOKI_ADDR` and `LOKI_ORG_ID` are listed in `logcli query --help`; `--from`, `--to`, `--parallel-*`, `--merge-parts`, `--part-path-prefix` flags exist. Ordering advice (selectors first, simple line filters before regex and parsers) matches the Loki query/bp-query page from the v3.7.9 docs source. The query-frontend sharding and bloom claims are gated as marked.
