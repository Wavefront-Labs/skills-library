---
id: computing-software.data-science-and-analytics.apache-superset.cache-warmup-and-thumbnails
name: cache-warmup-and-thumbnails
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [cache-warmup, thumbnails, celery-beat, executors, webdriver]
level: advanced
status: docs-checked
description: "Warm Superset caches with Celery beat strategies and run dashboard thumbnails: required settings, executors, freshness TTL and rollout order."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/configuration/cache.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pre-fill caches and generate thumbnails without surprising permissions.

Cache warm-up (Celery beat) requires `SUPERSET_CACHE_WARMUP_USER` and a persistent backend whose effective timeout is positive. Strategies:
- `top_n_dashboards` (for example top 5 with `since`).
- `native_filter_options` (takes `dashboard_ids`).
Schedule runs at least as often as the effective TTL. Cascading filters and search-term variants are not warmed.

Thumbnails:
- Feature flags `THUMBNAILS` and `THUMBNAILS_SQLA_LISTENERS`.
- `THUMBNAIL_EXECUTORS` and `CACHE_WARMUP_EXECUTORS` default to current-user and editor-based execution; use a `FixedExecutor` with a dedicated read-only service account instead.
- Related settings: `WEBDRIVER_BASEURL`, `WEBDRIVER_OPTION_ARGS`, `WEBDRIVER_AUTH_FUNC`, `MACHINE_AUTH_PROVIDER_CLASS`.
- `THUMBNAIL_UPDATED_CACHE_TTL` defaults to 604800 seconds (7 days); `0` or `None` disables the freshness check. It applies to the dashboard screenshot endpoint and to `compute-thumbnails` without `--force`.
- Roll out thumbnail workers before web servers, and keep web and worker `TZ` consistent.
- Thumbnail endpoints return `ETag`; a matching `If-None-Match` gets `304 Not Modified`.

Distributed coordination (separate skill) covers `DISTRIBUTED_COORDINATION_CONFIG`. The experimental semantic containment cache is off by default and needs `SEMANTIC_LAYER_CONTAINMENT_CACHE`, `SEMANTIC_LAYERS`, a shared persistent `DATA_CACHE_CONFIG` and Redis-backed coordination on every process; roll back by disabling the flag, restarting everything and confirming `semantic_cache.containment.enabled` reads zero.

## Checked

2026-11-08. Confirmed against the cited cache warm-up and thumbnails pages (read in full); no content changes needed.
Method: documentation only; no commands were run.
