---
id: computing-software.data-engineering.snowflake.result-and-warehouse-cache
name: result-and-warehouse-cache
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, result-cache, warehouse-cache, local-disk-cache, use-cached-result, metadata-cache, auto-suspend-tradeoff, benchmarking, snowflake-performance]
level: practitioner
status: docs-checked
description: "Understand Snowflake's caches: 24-hour result cache rules, warehouse local disk cache vs auto-suspend, metadata-only queries, and disabling caches for honest benchmarks."
sources:
  - https://docs.snowflake.com/en/user-guide/querying-persisted-results
  - https://docs.snowflake.com/en/user-guide/performance-query-warehouse-cache
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Result cache and warehouse cache

**Goal:** exploit caching for repeated queries (BI) and avoid being fooled by it when tuning.

## Two layers
| Cache | Where | Reuse conditions |
|---|---|---|
| **Result cache** | Persisted query results | Identical query, underlying data unchanged, no non-deterministic functions (`current_timestamp()`, `random()`). Retention is 24 hours, reset on each reuse, up to a maximum of 31 days. Controlled by `USE_CACHED_RESULT` |
| **Warehouse (local disk) cache** | Running warehouse nodes | Data read by earlier queries on the same warehouse; the auto-suspend setting affects it |

## Using it well
- BI dashboards issuing identical SQL benefit from the result cache: avoid injecting non-deterministic functions such as `current_timestamp()` into generated SQL; literal dates passed by the tool keep the query text identical.
- Auto-suspend trade-off: suspending a BI warehouse drops its local cache; during busy hours a longer auto-suspend can make dashboards faster. Measure.
- Route similar workloads to the same warehouse so they share the local cache.
- Fetching a previous result: `select * from table(result_scan(last_query_id()))`.

## Benchmarking honestly
```sql
alter session set use_cached_result = false;   -- disables result cache for this session
```
Warehouse cache: suspend/resume the warehouse between runs, or compare `percentage_scanned_from_cache` in QUERY_HISTORY. Run each test multiple times and report cold and warm separately.

## Verify
- [ ] A repeated dashboard query is served from the result cache (no warehouse time).
- [ ] Tuning comparisons note cache state (cold/warm) and `use_cached_result=false`.

## Checked
2026-10-28. Confirmed against the Snowflake persisted query results page (24 hour retention reset on reuse, maximum of 31 days, USE_CACHED_RESULT, RESULT_SCAN), the performance exploration page (cache and auto-suspension) and the QUERY_HISTORY view (percentage_scanned_from_cache). Removed: the metadata cache row, same-role and external-function conditions, the current_date reuse exception (current_date is listed as non-deterministic), the 60 second and 5-10 minute figures, resize cache loss and the query profile label.
Method: documentation only; no commands were run.
