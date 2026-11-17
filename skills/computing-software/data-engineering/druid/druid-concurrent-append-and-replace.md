---
id: computing-software.data-engineering.druid.druid-concurrent-append-and-replace
name: druid-concurrent-append-and-replace
category: computing-software
field: data-engineering
product: druid
tags: [concurrent-locks, append, replace, compaction, use-concurrent-locks]
level: advanced
status: docs-checked
description: "Enable concurrent append and replace so compaction and ingestion can share an interval."
sources:
  - https://github.com/apache/druid/blob/master/docs/ingestion/concurrent-append-replace.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Concurrent append and replace safely replaces data in an interval while new data is appended to it. The common use is appending streaming data to an interval while compaction of that interval is running. Data ingested during this time is partitioned with `dynamic` partitioning.

Turn it on with the context flag `useConcurrentLocks`; Druid then chooses the correct lock type, append or replace. You can set the lock type manually but the docs do not recommend it.

If you want to append while compaction runs, enable it in the compaction settings for the datasource. In the web console, open the datasource Compaction config and switch on Use concurrent locks. With the REST API, post to the Coordinator compaction config endpoint with a `taskContext`:

```shell
curl --location --request POST 'http://localhost:8081/druid/coordinator/v1/config/compaction' \
--header 'Content-Type: application/json' \
--data-raw '{
    "dataSource": "YOUR_DATASOURCE",
    "taskContext": {
        "useConcurrentLocks": true
    }
}'
```

The ingestion jobs themselves must also be configured to use concurrent locks: enable Use concurrent locks on the Publish step of the Load data wizard (classic batch and streaming), or add `"context": {"useConcurrentLocks": true}` to the supervisor or ingestion spec. To apply it to every ingestion and compaction job, set `druid.indexer.task.default.context={"useConcurrentLocks":true}` in the Overlord `runtime.properties`.

## Manual task lock types

Not recommended, but available as the `taskLockType` context parameter (types `APPEND` and `REPLACE`):
- The segment granularity of the append task must be equal to or finer than that of the replace task; otherwise concurrent append and replace fails.
- Only one task can hold a REPLACE lock on an interval; multiple tasks can hold APPEND locks on it.
- Streaming jobs always use APPEND. Use APPEND for dynamic partitioning with append to existing, and REPLACE for hash partitioning, range partitioning, or dynamic partitioning with append to existing false.
- Several appending jobs on one datasource running at once also need `"useSharedLock": "true"` (not with REPLACE; `taskLockType` takes precedence).

## Known limitations

Do not use it on a datasource with mixed granularity in any interval (for example both DAY and WEEK data), or whose compaction config compacts into more granular chunks than the ingested data (for example MONTH data compacted into DAY); either can cause data loss or duplication.

## Checked

Confirmed against the Druid docs page "Concurrent append and replace": the context flag, console and REST steps, Overlord default context, lock rules and limitations. Added the ingestion-job, lock-type and limitation sections the page states; the example request is as given there.

Method: docs-only read of cited pages, 2026-11-08
