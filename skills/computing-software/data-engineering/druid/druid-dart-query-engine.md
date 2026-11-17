---
id: computing-software.data-engineering.druid.druid-dart-query-engine
name: druid-dart-query-engine
category: computing-software
field: data-engineering
product: druid
tags: [dart, msq, broker, historical, parallel-sort-merge, experimental]
level: advanced
status: docs-checked
description: "Enable and tune Dart, the experimental Druid SQL engine that runs SELECT on Brokers and Historicals, and know its limits."
sources:
  - https://github.com/apache/druid/blob/master/docs/querying/dart.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dart is experimental and has had less testing than the other engines. It runs SELECT queries on Brokers and Historicals instead of tasks: a profile of MSQ where Brokers are controllers and Historicals are workers. It parallelizes throughout the query, so it excels at large joins (parallel sort-merge), high-cardinality exact groupBy and high-cardinality exact count distinct. By default Dart includes results from published segments and realtime tasks.

## Enable

Add to the `common.runtime.properties` files: `druid.msq.dart.enabled = true`.

## Resource settings (documented defaults)

Brokers (controllers need few resources):
- `druid.msq.dart.controller.concurrentQueries`: max concurrent controllers on that Broker; extras queue. Default 1. Queries can deadlock on each other if the Broker total exceeds a single Historical's worker setting.
- `druid.msq.dart.query.context.targetPartitionsPerWorker`: set equal to Historical `druid.processing.numThreads` to parallelize fully. Default 1 (multithreading off on Historicals).
- `druid.msq.dart.controller.syncPeriod`: how often Brokers sync running queries with Historicals. Default `PT15S`.

Historicals (do the processing; more resources mean faster queries):
- `druid.msq.dart.worker.concurrentQueries`: default equals the number of merge buffers; leave it. If changed, keep it at or above the Brokers' controller setting and not above the merge buffer count.
- `druid.msq.dart.worker.heapFraction`: heap share across all Dart queries. Default 0.35.
- `druid.msq.dart.worker.segmentLoadAheadCount`: segments prefetched ahead; a context value of `segmentLoadAheadCount` wins. Default unset (twice the processing threads).
- `druid.msq.dart.worker.controllerTimeout`: how long a Historical tolerates silence from a Broker before treating it as gone. Minimum `PT1M`, default `PT3M`.

## Running a query

- Console: Query view, engine selector **SQL (Dart)**.
- API: the SQL endpoint with context `engine` set to `msq-dart`, either in a `context` block or as `SET "engine"='msq-dart';` before the statement.

## Context parameters

Any SQL query context parameter works unless noted. Dart-relevant defaults: `finalizeAggregations` true; `includeSegmentSource` `REALTIME` for Dart (`NONE` for MSQ tasks); `removeNullBytes` false; `maxConcurrentStages` 2 for Dart (1 for MSQ tasks); `maxNonLeafWorkers` 1; `sqlJoinAlgorithm` `broadcast` (use `sortMerge` for big joins); `targetPartitionsPerWorker` 1 for Dart.

## Known limitations

- Does not verify `controller.concurrentQueries` is sane (too high can deadlock), does not use the query cache, does no prioritization or laning.
- TopN is always exact; `useApproximateTopN` unsupported.
- Not supported over the Avatica JDBC driver (the `engine` context is ignored); use the Druid JDBC driver.
- Realtime scans cannot reliably read complex types (for example HLL sketches), giving a `NullPointerException`.
- `NilStageOutputReader` can sometimes lead to `NoClassDefFoundError`.
- Broadcast joins with realtime data on the left are unsupported; set `sqlJoinAlgorithm` to `sortMerge`.

## Checked

2026-11-08. Read the cited Dart page in full. Replaced the thin draft with the full setting list, defaults, context parameters and known limitations from the page.

Method: documentation only; no commands were run.
