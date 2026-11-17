---
id: computing-software.data-engineering.apache-flink.checkpoint-failures-and-timeouts
name: checkpoint-failures-and-timeouts
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, checkpoints, checkpoint-timeout, checkpoint-alignment, tolerable-failed-checkpoints, backpressure, unaligned-checkpoints, state-size]
level: advanced
status: docs-checked
description: "Troubleshoot Flink checkpoints that expire or fail: read sync/async/alignment stats, relieve backpressure, tune timeouts, unaligned checkpoints and tolerable failures."
sources:
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/ops/monitoring/checkpoint_monitoring/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/ops/state/large_state_tuning/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/ops/state/checkpointing_under_backpressure/
  - https://github.com/apache/flink-connector-kafka/blob/main/docs/content/docs/connectors/datastream/kafka.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Checkpoint failures and timeouts

**Goal:** checkpoints complete reliably so recovery is quick and exactly-once sinks commit.

## Read the checkpoint stats (Web UI -> Checkpoints)
Per checkpoint and per subtask:
- **Sync duration:** the synchronous part of the checkpoint (snapshotting operator state); it blocks the subtask while it runs.
- **Async duration:** writing the checkpoint to the selected filesystem. Large = big state or slow storage.
- **Alignment duration / start delay:** time for barriers to arrive. Large = **backpressure** (barriers queue behind data).
- **Checkpointed data size** and **processed (persisted) in-flight data** (unaligned).
A checkpoint that takes longer than `execution.checkpointing.timeout` (default 10 min) is discarded.

## Fix by symptom
| Symptom | Fix |
|---|---|
| Long alignment/start delay | resolve backpressure (scale bottleneck operator, async I/O), enable **unaligned checkpoints** `execution.checkpointing.unaligned.enabled: true`, or buffer debloating `taskmanager.network.memory.buffer-debloat.enabled: true` |
| Long async phase, huge size | **incremental** checkpoints `execution.checkpointing.incremental: true`, state TTL, fix unbounded state growth |
| One subtask much slower | key skew -> that subtask has more state/data |
| Sink commit failures (Kafka transactions) | set the Kafka producer `transaction.timeout.ms` above the maximum checkpoint duration plus maximum restart duration |
| Checkpoint storage errors | S3 throttling: use entropy injection (`s3.entropy.key`, which replaces the key string in paths with random characters) |

## Key settings
```yaml
execution.checkpointing.interval: 60s
execution.checkpointing.timeout: 10min
execution.checkpointing.min-pause: 30s              # minimal pause between checkpoint attempts
execution.checkpointing.max-concurrent-checkpoints: 1
execution.checkpointing.tolerable-failed-checkpoints: 3   # don't fail job on a single expiry
execution.checkpointing.unaligned.enabled: true
execution.checkpointing.aligned-checkpoint-timeout: 30s   # start aligned, switch to unaligned if alignment exceeds this (0 = always unaligned)
execution.checkpointing.incremental: true
```
`execution.checkpointing.tolerable-failed-checkpoints` defaults to 0: no failure is tolerated, so a single expired checkpoint fails and restarts the job, which under backpressure can turn into a restart loop.

## Understand the cost of failures
No completed checkpoint = recovery replays from the last good one (more reprocessing), and exactly-once sinks hold uncommitted output (Kafka consumers in read_committed see nothing).

## Gotchas
- Unaligned checkpoints persist in-flight buffers: bigger checkpoints and extra I/O to the state storage.
- Very short intervals with large state = constant checkpointing load.

## Checked

2026-10-25 against the Apache Flink 2.3.0 documentation (release-2.3 branch on GitHub). Confirmed from the generated configuration tables (defaults: timeout 10 min, `tolerable-failed-checkpoints` 0, `max-concurrent-checkpoints` 1, `min-pause` 0 ms, `aligned-checkpoint-timeout` 0 ms, `unaligned.enabled` false, `execution.checkpointing.incremental` false), the checkpoint monitoring page (sync, async, alignment, start delay, in-flight data), the metrics reference (`numberOfFailedCheckpoints`, `lastCheckpointDuration`), the S3 page (`s3.entropy.key`) and the Kafka connector page (`transaction.timeout.ms`). Corrected `state.backend.incremental` to `execution.checkpointing.incremental` and the Kafka timeout rule; removed unconfirmed error text and version caveats.

Method: documentation only; no commands were run.

## Verify
- [ ] Checkpoint history: >99% completed; alignment and async durations stable.
- [ ] Alert on `numberOfFailedCheckpoints` increase and `lastCheckpointDuration` near timeout.
