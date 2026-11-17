---
id: computing-software.data-engineering.apache-flink.debugging-stuck-watermarks
name: debugging-stuck-watermarks
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, watermarks, stuck-watermark, idleness, currentinputwatermark, windows-not-firing, event-time, kafka-partitions]
level: advanced
status: docs-checked
description: "Debug Flink windows and timers that never fire: read watermark metrics per subtask, find idle partitions or bad timestamps, and fix with idleness, alignment or assigner changes."
sources:
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/dev/datastream/event-time/generating_watermarks/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/ops/debugging/debugging_event_time/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/ops/metrics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging stuck watermarks

**Goal:** explain why event-time windows/timers are not firing (or output stops) and fix the root cause.

## How watermarks combine
An operator's watermark = **minimum** of its input channels' watermarks. One input that never advances holds back everything downstream.

## Look at the numbers
The low watermark of each task is visible in the Web UI (choose a task in the metrics tab) and through the metrics system. Metrics:
- `currentInputWatermark`, `currentOutputWatermark` per operator/subtask.
- `watermarkAlignmentDrift` when watermark alignment is enabled.
A subtask whose watermark is missing or stuck in the past is the culprit; the downstream watermark is the minimum over all upstream subtasks.

## Common causes and fixes
| Cause | Signal | Fix |
|---|---|---|
| Idle Kafka partition / source split (no data) | one subtask watermark stuck, its input records = 0 | `WatermarkStrategy...withIdleness(Duration.ofMinutes(1))` |
| More source subtasks than partitions | some subtasks have no splits | parallelism <= partitions, or idleness |
| Timestamp assigner returns 0 / seconds instead of ms | watermark near epoch 1970 | fix assigner units |
| A far-future timestamp | watermark jumps ahead, then all data is "late" | validate/clamp timestamps before assigning |
| Watermarks assigned late in the pipeline instead of at the source | unexpected min across inputs | assign watermarks at the source (`fromSource(src, strategy, name)`), where per-split idleness and alignment work |
| Bounded out-of-orderness too large | windows fire hours late | reduce, handle stragglers with allowed lateness |
| Two-input operator (join/connect) with one slow/empty input | output stalls (its watermark is the minimum of both inputs) | idleness on that source |

## Watermark alignment (skewed sources)
If one partition races ahead (replaying backlog), downstream operators such as windows buffer data while waiting for the slowest. Watermark alignment pauses the source or split that gets too far ahead (FLIP-27 sources only); the arguments are group name, max allowed drift and update interval:
```java
WatermarkStrategy.<Event>forBoundedOutOfOrderness(Duration.ofSeconds(20))
    .withTimestampAssigner((e, t) -> e.tsMillis)
    .withIdleness(Duration.ofMinutes(1))
    .withWatermarkAlignment("orders-group", Duration.ofSeconds(30), Duration.ofSeconds(1));
```

## SQL jobs
`table.exec.source.idle-timeout` (default 0 ms, which disables idle detection) sets idleness for SQL sources, for example `SET 'table.exec.source.idle-timeout' = '1 min';`; watermarks come from `WATERMARK FOR ts AS ts - INTERVAL '5' SECOND` in DDL.

## Quick experiment
Temporarily add a `ProcessFunction` that logs `ctx.timerService().currentWatermark()` per subtask, or send a test event to every partition: if windows fire, it is idleness.

## Checked

2026-10-25 against the Apache Flink 2.3.0 documentation (release-2.3 branch on GitHub). Confirmed from the generating-watermarks page (idle sources, minimum over inputs, `withIdleness`, `withWatermarkAlignment(group, maxDrift, updateInterval)`, FLIP-27 restriction, two-input minimum), the event-time debugging page, the metrics reference (`currentInputWatermark`, `currentOutputWatermark`, `watermarkAlignmentDrift`) and the generated configuration table (`table.exec.source.idle-timeout`, default 0 ms). Removed the unconfirmed `watermarkLag` metric, the `No Watermark` UI label and the Kafka consumer and `noWatermarks()` advice.

Method: documentation only; no commands were run.

## Verify
- [ ] All subtasks' watermarks advance within the expected lag during quiet periods.
- [ ] Windows emit on time in a test with one empty partition.
