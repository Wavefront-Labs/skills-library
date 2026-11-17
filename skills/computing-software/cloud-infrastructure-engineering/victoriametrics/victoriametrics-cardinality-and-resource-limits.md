---
id: computing-software.cloud-infrastructure-engineering.victoriametrics.victoriametrics-cardinality-and-resource-limits
name: victoriametrics-cardinality-and-resource-limits
category: computing-software
field: cloud-infrastructure-engineering
product: victoriametrics
tags: [cardinality-limiter, max-hourly-series, resource-limits, capacity-planning, query-limits, high-churn]
level: advanced
status: docs-checked
description: "Cap series growth and query resource use with VictoriaMetrics cardinality and search limit flags and basic capacity rules."
sources: ["https://docs.victoriametrics.com/victoriametrics/single-server-victoriametrics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Victoriametrics cardinality and resource limits

Cardinality limiter: `-storage.maxHourlySeries` caps new series in the last hour and `-storage.maxDailySeries` in the last day. By default nothing is enforced. Setting either to `-1` (from v1.140.0) enables tracking without enforcement, which is useful for measuring before limiting. On vmagent the equivalents are `-remoteWrite.maxHourlySeries` and `-remoteWrite.maxDailySeries`.

Ingestion and label limits: `-maxIngestionRate`, `-maxLabelsPerTimeseries` (40), `-maxLabelValueLen` (4KiB).

Query limits: `-search.maxMemoryPerQuery`, `-search.maxUniqueTimeseries` (calculated automatically), `-search.maxQueryDuration`, `-search.maxConcurrentRequests`, `-search.maxQueueDuration`, `-search.maxSeries`, `-search.maxTagKeys`, `-search.maxTagValues`, and further `-search.max*` flags for samples, points, exports, federation and deletes. Memory for internal caches: `-memory.allowedPercent` or `-memory.allowedBytes`.

Query statistics: `-search.queryStats.lastQueriesCount` and `-search.queryStats.minQueryDuration` control the top-queries view. Query tracing is requested with `trace=1` and disabled with `-denyQueryTracing`.

Capacity planning rules: keep at least 50% free RAM, 50% spare CPU and 20% free disk in `-storageDataPath` (see `-storage.minFreeDiskSpaceBytes`). Use the cardinality explorer to find the metrics and labels driving series growth.

High availability: write with multiple vmagent instances and several `-remoteWrite.url` targets; read through vmauth load balancing or vmselect with `-dedup.minScrapeInterval=1ms` and `-replicationFactor=N`.

## Checked

2026-11-03. Flags, endpoints, HTTP paths, defaults, limits and version gates were checked against the official VictoriaMetrics documentation pages cited in `sources` (docs.victoriametrics.com, fetched this batch) with a phrase-by-phrase comparison. No wrong claims were found; no claims were removed.

Method: documentation only; no commands were run.
