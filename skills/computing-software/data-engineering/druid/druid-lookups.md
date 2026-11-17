---
id: computing-software.data-engineering.druid.druid-lookups
name: druid-lookups
category: computing-software
field: data-engineering
product: druid
tags: [lookups, dimension-values, join-like, current-data, one-to-one]
level: practitioner
status: docs-checked
description: "Use Druid lookups: LOOKUP vs JOIN, reverse-lookup and pull-up rewrites, injective flag, tiers, propagation and snapshot settings."
sources:
  - https://github.com/apache/druid/blob/master/docs/querying/lookups.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Lookups replace dimension values (key to value), giving join-like behaviour similar to a warehouse dimension table. They support one-to-one (country code to name) and many-to-one (many app ids to one account manager) mappings. Lookups have no history: a query always gets the current mapping regardless of time range. Time-range-sensitive mappings are not supported at query time; keep that data denormalized in the raw data.

Lookups are generally preloaded in memory on all servers. Very small ones (dozens to a few hundred entries) can be passed inline in native queries with the `map` lookup type. Other types come from extensions: globally cached lookups (local files, remote URIs, JDBC) and Kafka-topic lookups. Multi-value dimensions are not supported as keys: flatten them and map each element to the value.

## Querying

- SQL: `LOOKUP(store, 'store_to_country')`. The optional third argument `replaceMissingValueWith` is a constant string returned instead of NULL (equivalent to `COALESCE`).
- SQL JOIN: `INNER JOIN lookup.store_to_country ON sales.store = store_to_country.k` (columns `k` and `v`). `LOOKUP` has automatic rewrites that JOIN does not, so prefer it if they matter.
- Native: dimension specs or extraction functions.

## Query rewrites (LOOKUP only)

- Reverse lookup: `LOOKUP` in `WHERE` is rewritten to a filter on the key (`WHERE LOOKUP(sku,'sku_to_name') = 'WhizBang Sprocket'` becomes `WHERE sku = 'WB00013'`), so data servers can use indexes. Equality, `IN`, `IS NOT DISTINCT FROM` (non-null literals), `MV_CONTAINS`/`MV_OVERLAP` are reversible. Negations (`<>`, `NOT IN`) and `COALESCE(..., 'N/A') = 'N/A'` forms are reversible only for injective lookups. `IS NULL`, other wrapping functions, and `COALESCE` with a non-constant second argument are not reversible. Not applied when matching keys exceed `sqlReverseLookupThreshold` or `inSubQueryThreshold`. It adds planning time on large lookups (see the `sqlQuery/planningTimeMs` metric or time `EXPLAIN PLAN FOR`). Disable with `sqlReverseLookup: false` in the query context.
- Pull up: an injective lookup is applied after the `GROUP BY` (grouping by `sku` instead of the looked-up name). Disable with `sqlPullUpLookup: false`.
- Injective means all values unique, and a key defined for every input the call may see (null needs no key). Set `injective: true` in the lookup definition when true. Druid does not verify it; a wrong flag can return incorrect results.

## Dynamic configuration (via the Coordinator)

- Config is per lookup tier at `/druid/coordinator/v1/lookups/config/{tier}/{id}`. Lookup tiers are independent of Historical tiers (for example Historicals in `__default`, Peons in per-datasource tiers).
- If you have never configured lookups, POST an empty JSON object `{}` to `/druid/coordinator/v1/lookups/config` first.
- Responses: 404 not found, 400 bad format, 202 accepted asynchronously (POST and DELETE), 200 success (GET).
- The Coordinator propagates config to Broker, Router, Peon and Historical processes and checks periodically. A query-serving process handles only 2 concurrent propagation requests.
- Process properties: `druid.lookup.lookupTier` (default `__default`), `druid.lookup.lookupTierIsDatasource` (default false; mainly for Peons; if true do not set `lookupTier`).
- Coordinator manager: `druid.manager.lookups.hostTimeout` 2000 ms, `allHostTimeout` 900000 ms, `period` 120000 ms, `threadPoolSize` 10.
- Surviving restarts: `druid.lookup.snapshotWorkingDir` (default null, which disables snapshots), `enableLookupSyncOnStartup` (default true), `numLookupLoadingThreads` (available processors / 2), `coordinatorFetchRetries` 3, `lookupStartRetries` 3, `coordinatorRetryDelay` 60000 ms.

## Introspection

On a Broker, if the lookup type supports it: GET `/druid/v1/lookups/introspect/{lookupId}` (full map), `.../keys`, `.../values`.

## Checked

2026-11-08. Read the cited lookups page in full. Replaced the draft's heap-sizing note (it came from a page not cited here) with the page's query rewrites, injective rules, tier configuration, defaults and introspection endpoints.

Method: documentation only; no commands were run.
