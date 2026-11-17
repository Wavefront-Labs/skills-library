---
id: computing-software.data-engineering.apache-flink.batch-execution-mode
name: batch-execution-mode
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, batch-execution-mode, runtime-mode, bounded-streams, datastream-api, backfill]
level: practitioner
status: docs-checked
description: "Run Flink DataStream jobs in BATCH execution mode over bounded inputs: what changes (scheduling, state, watermarks, sinks), when to use it, and backfill patterns."
sources:
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/dev/datastream/execution_mode/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/ops/batch/batch_shuffle/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Batch execution mode

One DataStream program can run as streaming or batch. With all sources bounded, BATCH mode lets Flink use scheduling, shuffle and state strategies that need fewer resources than streaming.

```java
env.setRuntimeMode(RuntimeExecutionMode.BATCH);   // or AUTOMATIC: batch if all sources bounded
```
Prefer setting it at submit time so the same jar runs both ways: `flink run -Dexecution.runtime-mode=BATCH job.jar`.

## What changes in BATCH
| Aspect | STREAMING | BATCH |
|---|---|---|
| Scheduling | all tasks deployed at once | stage by stage; needs fewer slots |
| Shuffle | pipelined | blocking (intermediate results persisted; sort shuffle is a blocking implementation), or hybrid shuffle via `execution.batch-shuffle-mode` |
| Keyed state | state backend, kept for all keys | configured state backend is ignored; input is grouped by key (sorting) and only one key's state is kept at a time |
| Checkpoints | yes | none; on failure Flink backtracks to the latest available persisted intermediate results instead of restarting the whole job |
| Watermarks | progressive | only a `MAX_WATERMARK` at the end of the input; the watermark switches between `MAX_VALUE` and `MIN_VALUE` between keys, so do not assume it ascends in an operator |
| Processing-time timers | fire on wall clock | processing time does not advance during the job; timers fire at the end of the input |
| Output | incremental: rolling operations such as `reduce()` and `sum()` emit an update per record | rolling operations emit only the final result |
| Sinks | exactly-once via checkpoints | no checkpoints: Kafka `EXACTLY_ONCE` and `FileSink` `OnCheckpointRollingPolicy` do not work; a transactional sink must use the Unified Sink API (FLIP-143) |

## Consequences
- Logic relying on processing-time timers or early firings behaves differently; do not cache the last seen watermark in an operator, and operations that change a key manually are not supported.
- With several input types, broadcast inputs are processed first, then regular inputs, then keyed inputs; for several regular or broadcast inputs (for example `CoProcessFunction`) Flink may process them in any order.

## Backfill pattern
Same job code: run in BATCH over bounded input to rebuild a table, then start the STREAMING job at the matching offsets (or bootstrap state with the State Processor API).

## Table API/SQL
`SET 'execution.runtime-mode' = 'batch';` in the SQL client switches the runtime mode.

## Checked

2026-10-25 against the Apache Flink 2.3.0 documentation (release-2.3 branch on GitHub). Confirmed from the execution mode page, the batch shuffle page and the generated configuration table (`execution.runtime-mode`, `execution.batch-shuffle-mode`). Corrected the sink row (Kafka exactly-once does not work in BATCH); removed unconfirmed version gates, iteration support and the Kafka/JDBC bounded-source examples.

Method: documentation only; no commands were run.

## Verify
- [ ] Batch run output equals the streaming job's final output on the same bounded input.
- [ ] Slot usage and runtime lower than streaming over the same data.
