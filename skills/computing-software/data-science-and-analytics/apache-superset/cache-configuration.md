---
id: computing-software.data-science-and-analytics.apache-superset.cache-configuration
name: cache-configuration
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [cache, data-cache-config, filter-state, timeouts, redis]
level: practitioner
status: docs-checked
description: "Configure Superset caches: the four cache config keys, chart timeout precedence, native filter timeout, async TTL floor and the value size cap."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/configuration/cache.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: set up the caches Superset needs and tune their lifetimes.

Keys:
- `FILTER_STATE_CACHE_CONFIG` (dashboard filter state) and `EXPLORE_FORM_DATA_CACHE_CONFIG` (Explore form data) are required.
- `CACHE_CONFIG` (metadata) and `DATA_CACHE_CONFIG` (chart data) are optional.
- If the filter-state or explore cache is undefined, Superset falls back to a metastore cache. For chart data you can use `"CACHE_TYPE": "SupersetMetastoreCache"` with `CACHE_KEY_PREFIX` and `CACHE_DEFAULT_TIMEOUT`.
- Backends: Redis (recommended), Memcached, SimpleCache, MinIO/S3, filesystem, custom. When a backend is configured and goes down, Superset fails fast rather than degrading silently.

Chart timeout precedence: chart, then dataset, then database, then the `DATA_CACHE_CONFIG` default. `-1` disables chart-data caching at that level. Column-value and compatibility endpoints use the top-level `CACHE_DEFAULT_TIMEOUT`, so setting only the nested value to `-1` does not disable them.

`NATIVE_FILTER_OPTIONS_CACHE_TIMEOUT` (default `None`): `-1` disables, a positive integer is seconds, `0` is backend-specific (use `-1`). It does not override an explicit force-refresh timeout.

`GLOBAL_ASYNC_QUERIES_MIN_CACHE_TTL` (default `300`) raises shorter TTLs for async requests only so results are not evicted before the client reads them; longer TTLs and `0` (forever) are unchanged. Do not set it below your worst-case async round trip.

`DATA_CACHE_MAX_VALUE_SIZE` (bytes, default `None`) skips caching oversized values; the `skip_cache_value_too_large` statsd metric counts them.

SQL Lab results use `RESULTS_BACKEND`, a cachelib object rather than a Flask-Caching dict.

## Checked

2026-11-08. Confirmed against the Caching page (read in full); no content changes needed.
Method: documentation only; no commands were run.
