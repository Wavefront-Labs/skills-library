---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.refresh-interval-and-translog
name: refresh-interval-and-translog
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, refresh-interval-and-translog]
level: advanced
status: docs-checked
description: "Set index.refresh_interval, the refresh request parameter and translog durability, sync_interval and flush threshold in Elasticsearch, knowing the safety trade-offs."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/rest-apis/refresh-parameter
  - https://www.elastic.co/docs/reference/elasticsearch/index-settings/translog
  - https://www.elastic.co/docs/deploy-manage/production-guidance/optimize-performance/indexing-speed
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Refresh interval and translog durability (Elasticsearch)

**Goal:** pick near-real-time search latency versus indexing throughput, and know what a crash can lose. Scope: Elasticsearch docs; OpenSearch settings were not checked here, so confirm names and defaults in the OpenSearch reference for your version.

## Refresh
- `index.refresh_interval` is dynamic. Default is `1s` in the Elastic Stack and `5s` in Elastic Cloud Serverless (where it must be `-1` or at least `5s`).
- By default Elasticsearch only refreshes every second on indices that have received at least one search request in the last 30 seconds. Set the interval explicitly to opt out of that behaviour.
- If you have regular search traffic and can tolerate delay, a larger value such as `30s` can improve indexing speed. For a large bulk load, set `"refresh_interval": "-1"` via `PUT <index>/_settings`, then restore it (for example `5s`) afterwards; documents are not searchable while disabled. Consider a force merge after bulk loading (expensive).
- Request-level `refresh` on the Index, Update, Delete and Bulk APIs: `false` (default) does nothing; `true` (or empty) refreshes the affected shards immediately and should only be used after careful thought; `wait_for` waits for the next scheduled refresh before replying.
- `refresh=true` creates tiny segments that must be merged later, costing at index, search and merge time.
- Do not issue multiple `wait_for` requests in a row; batch them into one bulk request with `refresh=wait_for`. With `refresh_interval` set to `-1`, `wait_for` waits indefinitely until something causes a refresh. If `index.max_refresh_listeners` (default 1000) requests are already waiting on a shard, a `wait_for` request forces a refresh and the response contains `"forced_refresh": true`.

## Translog
- Each shard copy writes operations to a translog before acknowledging them; after a crash, acknowledged operations not yet in the last Lucene commit are recovered from it. A flush performs a Lucene commit and starts a new translog generation.
- `index.translog.durability`: `request` (default) fsyncs and commits after every index, delete, update or bulk request on the primary and every allocated replica; `async` fsyncs every `index.translog.sync_interval` (default `5s`, minimum `100ms`), so acknowledged writes since the last commit can be lost on failure.
- `index.translog.flush_threshold_size` (default 10 GB) caps the unflushed operations so recovery does not take too long.

## Verify
- [ ] A just-indexed document appears in search only after the next refresh (or immediately with `refresh=wait_for` on the write).
- [ ] The translog durability of each index matches the data-loss tolerance agreed for it.

## Notes
- Try every request on a test index first.

## Checked
2026-11-08. Confirmed against the Elasticsearch "The refresh parameter", "Translog settings" and "Tune for indexing speed" pages: refresh defaults, wait_for behaviour, forced_refresh, max_refresh_listeners, durability values, sync_interval, flush threshold. Removed: OpenSearch applicability (not checked) and the earlier generic reference links.
Method: documentation only; no commands were run.
