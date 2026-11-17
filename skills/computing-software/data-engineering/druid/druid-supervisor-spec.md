---
id: computing-software.data-engineering.druid.druid-supervisor-spec
name: druid-supervisor-spec
category: computing-software
field: data-engineering
product: druid
tags: [supervisor, streaming-ingestion, supervisor-spec, kafka, kinesis, autoscaler]
level: practitioner
status: docs-checked
description: "Write a Druid streaming supervisor spec: ioConfig and tuning defaults, task autoscaler, capacity planning, status states, reset and suspend."
sources:
  - https://github.com/apache/druid/blob/master/docs/ingestion/supervisor.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Supervisors manage streaming ingestion: they oversee indexing tasks to coordinate handoffs, manage failures and keep scalability and replication requirements. They can also run automatic compaction. Offset (Kafka) is the same idea as sequence number (Kinesis).

## Spec properties

- `id`: defaults to `spec.dataSchema.dataSource`.
- `type` (required): `kafka`, `kinesis` or `rabbit` for streaming, `autocompact` for compaction.
- `spec` (required): container; for compaction it is the compaction configuration.
- `spec.dataSchema` and `spec.ioConfig` required; `spec.tuningConfig` optional.
- `context`: extra config for the supervisor and its tasks. `suspended`: boolean, starts the supervisor suspended.

## Common ioConfig (defaults)

- `inputFormat` required. `taskCount` 1 (max reading tasks per replica set; capped by Kafka partitions or Kinesis shards). `replicas` 1 (replicas land on different workers).
- `taskDuration` `PT1H`; `startDelay` `PT5S`; `period` `PT30S` (max time between management iterations); `completionTimeout` `PT30M` (too low and tasks may never publish).
- Late/early rejection: `lateMessageRejectionStartDateTime`, `lateMessageRejectionPeriod` (specify only one late property), `earlyMessageRejectionPeriod`. No defaults. Useful when a nightly batch pipeline touches the same segments.
- `stopTaskCount`: limits how many tasks cycle at once; default is the `taskCount` value. Lower values need fewer free slots but slow cycling and add lag. Changes to the spec or Kafka partition count still cycle all tasks, and the autoscaler ignores it when changing task count.
- `serverPriorityToReplicas`: map of `druid.server.priority` to replica count for query isolation, for example `{"1": 2, "0": 1}`; if `replicas` is also set the sum must equal it. Scales with `taskCount`.
- `boundedStreamConfig`: one-time ingestion between `startSequenceNumbers` (inclusive) and `endSequenceNumbers` (exclusive for Kafka, inclusive for Kinesis). The supervisor reaches `COMPLETED` and terminates. The bounds are stored with datasource metadata; a restart or new supervisor with different offsets for the same datasource fails, so reset the supervisor or use a different id.

## Task autoscaler (`ioConfig.autoScalerConfig`)

- `enableTaskAutoScaler` defaults `false` even when the object is present. `taskCountMax` and `taskCountMin` required. Initial count comes from `taskCountStart`, then `taskCount`, then `taskCountMin`.
- `minScaleUpDelay`, `minScaleDownDelay` (ISO 8601; fall back to deprecated `minTriggerScaleActionFrequencyMillis`, 600000). `autoScalerStrategy` `lagBased` (default) or `costBased`. `stopTaskCountRatio` in (0.0, 1.0].
- `lagBased` defaults: `lagCollectionIntervalMillis` 30000, `lagCollectionRangeMillis` 600000, `scaleOutThreshold` 6000000, `triggerScaleOutFractionThreshold` 0.3, `scaleInThreshold` 1000000, `triggerScaleInFractionThreshold` 0.9, `scaleActionStartDelayMillis` 300000, `scaleActionPeriodMillis` 60000, `scaleInStep` 1, `scaleOutStep` 2, `lagAggregate` `SUM` (or `MAX`, `AVERAGE`). Kinesis lag is in milliseconds, not messages.
- `costBased`: picks the task count with the lowest combined lag cost and idle cost (target about 25% idle). Defaults: `scaleActionPeriodMillis` 120000, `lagWeight` 0.4, `idleWeight` 0.6, `useTaskCountBoundariesOnScaleUp` false, `useTaskCountBoundariesOnScaleDown` true, `minScaleUpDelay` `PT15M`, `minScaleDownDelay` `PT30M`, `scaleDownDuringTaskRolloverOnly` false, `criticalLagThreshold` null (disabled), `highLagCostFactor` 6.0. At 75% of `criticalLagThreshold` the high-lag cost factor applies; at 100% it jumps to `taskCountMax`. Units: records for Kafka and Rabbit, milliseconds for Kinesis.

## Common tuningConfig (defaults)

- `type` required (`kafka` or `kinesis`). `maxRowsInMemory` 150000 (post-aggregation rows). `maxBytesInMemory` one-sixth of max JVM memory. Heap use scales as the in-memory limit times (2 + `maxPendingPersists`).
- `maxRowsPerSegment` 5000000; `maxTotalRows` 20000000; `intermediateHandoffPeriod` `P2147483647D`; `intermediatePersistPeriod` `PT10M`; `maxPendingPersists` 0.
- `handoffConditionTimeout` 900000 ms for Kafka, 0 (wait indefinitely) for Kinesis. `resetOffsetAutomatically` false. `workerThreads` `min(10, taskCount)`. `chatRetries` 8. `httpTimeout` `PT10S`. `shutdownTimeout` `PT80S`. `offsetFetchPeriod` `PT30S` (minimum `PT5S`).
- Parse errors: `logParseExceptions` false, `maxParseExceptions` unlimited, `maxSavedParseExceptions` 0. `reportParseExceptions` is deprecated and overrides the other two when true.
- `maxColumnsToMerge` -1. Kafka- and Kinesis-specific properties are on their own pages.

## Lifecycle

- Submit via the web console data loader or the Supervisor API. The supervisor persists in the metadata database; submitting the same id overwrites it. A new Overlord leader respawns supervisors and adopts compatible running tasks, terminating incompatible ones.
- Schema or config changes: submit a new spec. The old supervisor tells tasks to stop reading and publish, and the new one starts tasks at the previous offsets, so ingestion is not paused.
- Suspend pauses it (logs and metrics continue). Set offsets and hard reset can skip or duplicate data; hard reset clears metadata and resumes from earliest or latest per `useEarliestOffset`. Terminate stops the supervisor and tasks, publishes segments and leaves a tombstone in metadata.
- Several supervisors can ingest one datasource; set `useConcurrentLocks=true` in the spec `context`.

## Status

- Report holds `state`, `detailedState` and `recentErrors` (size via `druid.supervisor.maxStoredExceptionEvents`). `state` values: `PENDING`, `RUNNING`, `SUSPENDED`, `STOPPING`, `UNHEALTHY_SUPERVISOR`, `UNHEALTHY_TASKS`; `detailedState` also includes `UNABLE_TO_CONNECT_TO_STREAM`, `LOST_CONTACT_WITH_STREAM`, `IDLE` and first-iteration states. Unhealthy thresholds are `druid.supervisor.unhealthinessThreshold` and `druid.supervisor.taskUnhealthinessThreshold`.
- Query `sys.supervisors` for health, for example `WHERE healthy=0`.
- Per-partition Kafka lag can show negative if the latest offset has not arrived; aggregate lag is always >= 0.

## Capacity planning

Tasks run on Middle Managers; worker capacity (`druid.worker.capacity`) is shared by all task types. Reading tasks are `replicas * taskCount`. Minimum capacity for reading and publishing sets to overlap is `workerCapacity = 2 * replicas * taskCount`. If time to publish exceeds `taskDuration` more sets publish at once and need more capacity. Out-of-capacity tasks queue; queries may return partial results but no data is lost if offsets remain in the stream.

## Checked

2026-11-08. Read the cited supervisor page in full. Rewrote the draft: added documented defaults for ioConfig, autoscaler and tuningConfig, bounded ingestion, lifecycle actions, status states and capacity formula. Cost-based and lag-based example specs on the page are not reproduced.

Method: documentation only; no commands were run.
