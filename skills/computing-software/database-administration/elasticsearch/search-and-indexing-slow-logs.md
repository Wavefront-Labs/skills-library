---
id: computing-software.database-administration.elasticsearch.search-and-indexing-slow-logs
name: search-and-indexing-slow-logs
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, search-slow-log, indexing-slow-log, slowlog-thresholds, query-phase, fetch-phase, profile-api, search-performance]
level: practitioner
status: docs-checked
description: "Configure Elasticsearch search and indexing slow logs per index with phase thresholds, read the entries, and follow up with the profile API."
sources:
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/monitor/logging-configuration/slow-logs.md
  - https://github.com/elastic/elasticsearch/blob/main/docs/reference/elasticsearch/index-settings/slow-log.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Search and indexing slow logs

**Goal:** find which queries and bulk requests are slow, with their source, per shard.

## Enable (dynamic, per index or via template)
```json
PUT orders/_settings
{
  "index.search.slowlog.threshold.query.warn": "2s",
  "index.search.slowlog.threshold.query.info": "500ms",
  "index.search.slowlog.threshold.fetch.warn": "1s",
  "index.search.slowlog.include.user": true,
  "index.indexing.slowlog.threshold.index.warn": "1s",
  "index.indexing.slowlog.source": "1000",
  "index.indexing.slowlog.reformat": true
}
```
Slow logs are off by default (all thresholds are `-1`), and each log level (`warn`, `info`, `debug`, `trace`) has its own threshold. Put them in an index template (`template.settings`) so new time-based indices inherit them. For searches, query logging is a documented unified alternative that records end-to-end request duration.

## Where it goes
`<cluster>_index_search_slowlog.json` and `<cluster>_index_indexing_slowlog.json` in the logs dir of the data node holding the shard. Entries include the index and shard, `elasticsearch.slowlog.took`, `total_hits`, `search_type` and the query `source`; with `include.user` they also carry `user.*` and `auth.type`, and an `X-Opaque-Id` request header appears in search slow logs as `elasticsearch.slowlog.id`. Files are written under the Elasticsearch logs directory (`log4j2.properties` controls destinations; the loggers are `index.search.slowlog` and `index.indexing.slowlog.index`, set to `trace` by default).

## Query vs fetch
- Query phase thresholds (`threshold.query.*`) and fetch phase thresholds (`threshold.fetch.*`) are separate settings; compare which one fires to see where the time goes. Treat the cause lists (expensive queries, large `_source`, many hits) as general tuning heuristics.

## Tag requests
Send an `X-Opaque-Id` header (for example `report-daily-sales`) from clients; it is included in search slow logs so you can tell which app sent the query.

## Next step: profile
```json
GET orders/_search
{ "profile": true, "query": { ... } }
```
Per-shard timing breakdown of query components and collectors (Kibana Search Profiler visualises it).

## Gotchas
- Slow logs report task duration at the shard level for searches and at the index level for indexing, and may not cover the full time the client sees; a request spanning many shards can be slow overall with no single shard over the threshold.
- `index.indexing.slowlog.source` records document `_source` (the docs example uses `"1000"` characters); use it only while troubleshooting, since it can increase log size and expose sensitive data.

## Verify
Set `threshold.query.trace` to `0ms` briefly on a test index, run a search, and see the entry in the search slow log; then restore.

## Checked

Checked 2026-10-25 against elastic/docs-content and elastic/elasticsearch `main` (Stack 9.x docs). Confirmed: threshold setting names for search (`query`, `fetch`) and indexing, `include.user`, `indexing.slowlog.source` and `reformat`, off by default (`-1`), file name suffixes, loggers and `trace` default, shard-level versus index-level scope, `X-Opaque-Id` in search slow logs as `elasticsearch.slowlog.id`. The `PUT orders/_settings` example uses thresholds of your choosing; the profile API advice and the `0ms` trace verification step were not re-read.

Method: documentation only; no commands were run.
