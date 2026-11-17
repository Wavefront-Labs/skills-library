---
id: computing-software.data-engineering.druid.druid-auto-compaction-setup
name: druid-auto-compaction-setup
category: computing-software
field: data-engineering
product: druid
tags: [auto-compaction, compaction-supervisor, coordinator-duties, overlord, compaction-config]
level: practitioner
status: docs-checked
description: "Set up Druid automatic compaction with Overlord compaction supervisors or Coordinator duties, including MSQ limits and ingestion conflicts."
sources:
  - https://github.com/apache/druid/blob/master/docs/data-management/automatic-compaction.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Compaction is a special ingestion task that reads from a datasource and writes back to the same datasource, normally to size segments well. Auto-compaction issues those tasks for you. The docs advise setting it up for all datasources. Manual compaction remains useful to give a job more resources (for example several parallel tasks for a first-time compaction). Auto-compaction skips datasources whose segment granularity is `ALL`.

Configuration is dynamic; no restart is needed.

## Two mechanisms

- Compaction supervisors on the Overlord (recommended): supervisor status and suspend/resume, native or MSQ engine, submits tasks as soon as a slot is free, tracks task status to avoid re-compacting an interval repeatedly, can store compaction fingerprints instead of full state, and supports minor compaction via the most-fragmented-first policy.
- Coordinator duties: the alternative. Requires the compaction dynamic config `useSupervisors` set to `false` and `engine` set to `native` (MSQ is not supported in the Coordinator).

## Config shape

The config `type` picks the schema source: `inline` (default; schema in the config) or `catalog` (schema read from the datasource's catalog table definition on every run, so editing the definition can rewrite stored data; a catalog config accepts only `dataSource`, `engine`, `skipOffsetFromLatest`, `skipIntervals`, `taskPriority`, `taskContext`, `inputSegmentSizeBytes`).

An inline config takes `dataSource`, `ioConfig`, `dimensionsSpec`, `transformSpec`, `metricsSpec`, `tuningConfig`, `granularitySpec`, plus the auto-compaction-only `skipOffsetFromLatest`, `skipIntervals`, `taskPriority`, `taskContext`. The system sets the generated task's own type (`compact`), its id (prefixed `auto`) and its context.

Performance tip from the docs: compaction tasks fetch all relevant segments before launching subtasks unless `granularitySpec` (non-null `segmentGranularity`, `queryGranularity`, `rollup`), `dimensionsSpec` and `metricsSpec` are all set. Setting them is strongly recommended.

## Using supervisors

Submit the config as a supervisor spec, via the web console (Supervisors tab, Submit JSON supervisor) or the supervisor API (POST to `/druid/indexer/v1/supervisor`), with `"type": "autocompact"` and the config in `spec` (optional `suspended`). If `spec.engine` is omitted, the cluster compaction dynamic config `engine` applies, and if that is also unset Druid uses `native`. Stop compaction by suspending or terminating the supervisor.

MSQ engine requirements: incremental segment metadata caching enabled on the Overlord; compaction supervisors in use; `engine` set to `msq` in the compaction dynamic config or `spec.engine`; at least two compaction task slots or `spec.taskContext.maxNumTasks` of 2 or more (one controller plus one worker). MSQ context parameters can go in `spec.taskContext`; where they overlap with auto-compaction parameters, set only one.

MSQ limitations: `metricsSpec` only supports aggregators that are mergeable and idempotent (for example `longSum` with the same input and output column name; not `longSum` that writes a different output column, `HLLSketchBuild`, or `count`); only dynamic and range partitioning; set `rollup` true if and only if the metrics spec is non-empty; partition only on single-valued string dimensions; no `maxTotalRows` in `DynamicPartitionsSpec` (use `maxRowsPerSegment`); sort only with `__time` first.

## Using Coordinator duties

- Frequency follows `druid.coordinator.period.indexingPeriod` (default 30 minutes), which also drives other duties such as unused-segment cleanup. To run compaction on its own schedule, define a duty group in `coordinator/runtime.properties`, for example `druid.coordinator.dutyGroups=["compaction"]`, `druid.coordinator.compaction.duties=["compactSegments"]`, `druid.coordinator.compaction.period=PT60S` (the docs' 1-minute example).
- If a compaction task outlasts the period, the Coordinator waits for it before resuming segment search.
- Enable via the web console (Datasources, Compaction column) or POST to `/druid/coordinator/v1/config/compaction`; disable with DELETE on `/druid/coordinator/v1/config/compaction/{dataSource}` (the config is not retained). Status: GET `/druid/coordinator/v1/compaction/status`, optionally `?dataSource=`.

## Avoiding conflicts with ingestion

If compaction keeps failing because ingestion needs a locked interval, choose one:
- Concurrent append and replace: `"useConcurrentLocks": true` in the compaction `taskContext` and in the ingestion jobs' context.
- `skipOffsetFromLatest`: measured back from the end of the most recent segment, not from now (for example `P5D`). A few hours to a day is reasonable for most streams.
- `skipIntervals`: exclude intervals (for example a backfill target), such as `["2015-04-01/2015-04-02"]`.
- Raise `taskPriority` above ingestion: advanced; can make ingestion fail or lag.

## Examples from the page

- Hourly segments to daily, leaving the latest week alone: `granularitySpec.segmentGranularity` `DAY` with `skipOffsetFromLatest` `P1W`.
- Repartition to multi-dimension range partitioning: `tuningConfig.partitionsSpec` of type `range` with `partitionDimensions` and `targetRowsPerSegment` (the page uses 5000000). The `channel`, `countryName`, `namespace` dimensions are example values.

## Checked

2026-11-08. Read the cited automatic-compaction page in full. Rewrote the draft with the config shape, both mechanisms' requirements, MSQ limitations and the conflict-avoidance options; example values are labelled as examples.

Method: documentation only; no commands were run.
