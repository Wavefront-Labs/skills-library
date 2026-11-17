---
id: computing-software.data-science-and-analytics.apache-superset.partition-filter-mapping
name: partition-filter-mapping
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [partition-filter-mapping, partition-pruning, transform, experimental, rate-limit]
level: sme
status: docs-checked
description: "Use experimental PARTITION_FILTER_MAPPING so filters on a column also prune a partition column via a :value transform; probe cache and limits."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/configuration/partition-filter-mapping.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let a filter on a business column (for example an event time) also filter the table's technical partition column so the engine prunes partitions.

Status: experimental, off by default. Enable with a static boolean `FEATURE_FLAGS = {"PARTITION_FILTER_MAPPING": True}`. Do not use a callable there (it is not evaluated and counts as truthy); if you use `GET_FEATURE_FLAGS_FUNC` or `IS_FEATURE_ENABLED_FUNC` the answer must be the same for every user, or a cached chart result built from pruned SQL could reach a user without the feature.

Configure: in the dataset editor, Columns tab, Default Column Settings, pick a Partition column (it follows the default datetime column unless overridden). On the mapped column set the value transform: one scalar SQL expression containing `:value`. Examples from the docs: `CAST(floor(:value / 86400) * 86400 AS BIGINT)` for epoch seconds into UTC day-start keys, `lower(:value)` for a lowercase region key. Enter the expression your pipeline really uses, including units and timezone.

Which filters mirror:
- `=` and `IN`: yes, except on text columns whose engine compares loosely (MySQL, SQL Server, Redshift), CHAR types, and coarse date comparisons with a time of day.
- `>`, `>=`, `<`, `<=` and time ranges: only if you tick Transform preserves ordering (non-decreasing; a strict bound mirrors non-strictly). Hour or day-of-week style transforms do not preserve ordering.
- `!=`, `NOT IN`, `LIKE`, `ILIKE`, `IS NULL`, `IS TRUE`: never.
- Not mirrored: filter-value dropdowns, row-level security, custom SQL WHERE, advanced data types, array partition columns. Native and cross filters do mirror. Non-ISO 8601 datetimes and values with a UTC offset do not mirror on coarse-comparison columns or at all, respectively.

Transform rules: refused on save if it has its own FROM or a subquery, `:value` inside a string literal or comment, over 1,024 characters, writes data, or calls non-deterministic functions (`now()`, `current_date`, `rand()`, zero-argument `unix_timestamp()`). No Jinja. Only the mapped column may carry a transform. On Hive/Impala a bare `unix_timestamp(:value)` is declined because it gives an instant, not a bucket.

Evaluation: Superset evaluates the transform against the engine and emits the result as a literal. Results are cached for `PARTITION_TRANSFORM_PROBE_CACHE_TIMEOUT` (24 hours by default). Preview requests are limited by `PARTITION_TRANSFORM_PREVIEW_RATE_LIMIT` (default 30 per user per dataset per minute). Both, and the pruning indicator, use `CACHE_CONFIG`, whose default is NullCache, so configure a shared backend (Redis or Memcached); `DATA_CACHE_CONFIG` does not help. If evaluation fails no predicate is added: the query is still correct, just scans more.

Safety: the mirror is only valid if the partition column always equals the transform of the mapped column in your data. Confirm with the pipeline owner, use Validate against data (samples at most 50 rows from one to three numeric partition keys), and compare results with and without the predicate before production. Superset adds `OR partition IS NULL` so NULL-partition rows are kept. If a partition column is dropped in the warehouse, run Sync columns from source; Superset retries a rejected chart query once without the mirror. View query shows the added predicate.

## Checked

2026-11-08. Confirmed against the Partition Filter Mapping page (read in full). Removed: "unsupported operators are not mapped" vagueness, "validate in SQL Lab" and "keep the flag off in production" advice (the page says confirm the pipeline invariant and validate against data); the page's engine-specific timezone and per-engine coercion details were summarised, not reproduced.
Method: documentation only; no commands were run.
