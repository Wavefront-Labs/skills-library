---
id: computing-software.data-engineering.druid.druid-query-caching
name: druid-query-caching
category: computing-software
field: data-engineering
product: druid
tags: [caching, per-segment-cache, whole-query-cache, memcached, cache-invalidation]
level: practitioner
status: docs-checked
description: "Choose Druid per-segment or whole-query caching, where to enable each, and when caching will not help."
sources:
  - https://github.com/apache/druid/blob/master/docs/querying/caching.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Query caching speeds up frequently accessed data and is in addition to data-level segment caching on Historicals. Hit rate and evictions appear in Druid metrics, so watch them when tuning.

## Cache types

- Per-segment cache: partial results per segment, enabled by default on Historicals; controlled by the query parameters `useCache` and `populateCache`. Good for segments that rarely change. Real-time segments are computed at query time, and cached Historical results are merged with real-time results, so use it with streaming data. Cached results may also merge into later queries of a similar shape (for example a different time period).
- Whole-query cache: final results cached on the Broker, so the Broker skips merging per-segment results. Use it where ingestion rarely invalidates segments (for example batch data). With real-time ingestion new data keeps invalidating the whole result.
- Druid invalidates a cache the moment underlying data changes, which matters most for table datasources with fast-changing segments.
- Storage: local JVM heap (default Caffeine, default maximum the minimum of 1 GiB and ten percent of max JVM memory, no expiry, least-recently-used eviction once full) or an external key/value store such as memcached.

## Where to enable

- Per-segment: on Historicals (default; they merge their own results, easing Broker load, recommended for larger clusters), on Peon/Indexer task services (local caches only such as Caffeine; remote types like memcached are ignored because partial segments can differ across task replicas), or on Brokers only for small clusters under five servers.
- Avoid Broker per-segment caching on large clusters: with `druid.broker.cache.populateCache` true and `populateCache` not false in the query context, Historicals stop merging and pass segment results to the lead Broker, which must do one large merge.
- Whole-query cache: Brokers only.

## Performance expectations

- Caching mainly raises concurrency for mixed workloads. To speed up a single query or page load, ignore it; the cold-cache time should already meet targets.
- Per-segment cache hits bypass data server processing threads. Gains are largest for `topN` and timeseries; groupBy merge bottlenecks on the Broker see less benefit, likewise joins.
- Per-segment caching does not work for: queries containing a sub-query (sub-query output may be cached), joins on the Broker, groupBy segment-level caching on the Broker, and `bySegment` queries on the Broker.
- Whole-query caching does not work for: inline or lookup datasources, joins, union datasources.

Configuration properties live in the cache configuration reference and the "using query caching" page, which this page links to.

## Checked

2026-11-08. Read the cited caching overview page in full. Expanded the draft with where-to-enable rules, defaults and unsupported cases. Configuration property tables are on a separate page that was not read, so none are listed here.

Method: documentation only; no commands were run.
