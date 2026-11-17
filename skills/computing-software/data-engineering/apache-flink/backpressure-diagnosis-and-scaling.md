---
id: computing-software.data-engineering.apache-flink.backpressure-diagnosis-and-scaling
name: backpressure-diagnosis-and-scaling
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, backpressure, buffer-debloating, busytime, idletime, parallelism, task-slots, flink-reactive-mode, autoscaling, flink-kubernetes-operator, checkpoint-alignment, network-buffers, flink-ui, metrics]
level: practitioner
status: docs-checked
description: "Diagnose Flink backpressure and operator bottlenecks with the Flink UI/metrics, and scale parallelism and resources correctly."   # quoted: YAML would cut an unquoted value at " #" or choke on ": "
sources:
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/ops/monitoring/back_pressure/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/ops/metrics/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/deployment/elastic_scaling/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnosing Flink backpressure and scaling correctly

**Goal:** find which operator is actually the bottleneck (not the one that merely shows symptoms of it) and fix it with the right scaling lever.

## 1. Read backpressure right-to-left
Flink backpressure propagates **upstream**: a slow downstream operator fills its input buffers, which blocks the upstream operator's output, which blocks the operator before it, and so on back to the source. A task showing back pressure (black in the UI JobGraph) is being slowed by something downstream, so it is not the bottleneck itself; look at the downstream tasks. The bottleneck is typically the first task, walking downstream from the source, that is fully busy (red) but not back pressured.

## 2. Use the metrics, not just the UI's sampled indicator
Each subtask exposes `busyTimeMsPerSecond`, `idleTimeMsPerSecond` and `backPressuredTimeMsPerSecond`; together they add up to about 1000 ms. They are averaged over the last couple of seconds, so a bursty load can hide behind a mid-range value. The UI JobGraph shows the maximum of each across subtasks (idle blue, fully back pressured black, fully busy red), and the *Back Pressure* tab shows per-subtask status (OK up to 10% back pressured, LOW up to 50%, HIGH above 50%). The same metrics can be scraped through a metrics reporter. A task near 1000 ms busy with near-zero back pressured time downstream of a back pressured chain is the likely bottleneck.

## 3. Common root causes, not just "add parallelism"
- **Skewed keys**: one subtask processes far more records than its siblings (hot key). Check per-subtask `numRecordsIn` — if one subtask is far above the others, parallelism increases won't help; you need a better key or a two-phase aggregation (local pre-aggregate on a salted key, then combine).
- **Slow external I/O in a `RichFunction`** (sync DB lookup per record, blocking HTTP enrichment call): this stalls the whole chained operator regardless of parallelism. Use Flink's **Async I/O** (`AsyncDataStream.unorderedWait`) to overlap in-flight requests instead of adding slots.
- **Checkpoint alignment stalls**: under severe backpressure with aligned checkpoints, checkpoint barriers queue behind data and checkpoints slow or time out. Consider **unaligned checkpoints** (`execution.checkpointing.unaligned.enabled: true`) so barriers skip ahead of buffered data, and buffer debloating (`taskmanager.network.memory.buffer-debloat.enabled`) to shrink in-flight data.
- **Undersized network buffers** choke throughput before CPU is the limit — check `outPoolUsage`/`inPoolUsage` near 100% as a sign buffers, not compute, are the ceiling; consider raising `taskmanager.memory.network.fraction`.

## 4. Scaling levers, in order of cost
1. Fix the actual bottleneck operator (async I/O, key salting, skip a wasteful serialization) — always cheaper than adding hardware.
2. Increase that operator's parallelism alone via `setParallelism()` per-operator if the job doesn't need uniform parallelism — don't blanket-scale the whole job to fix one slow operator.
3. **Reactive Mode** (standalone application deployments only) or an external autoscaler adjusts parallelism automatically; verify scale-down behaviour does not thrash on normal load dips.
4. Vertical scaling (bigger TM memory/CPU) only helps when the bottleneck is genuinely resource-bound (GC pauses, RocksDB I/O wait), not when it's a skew or serialization problem that more CPU won't fix.

## Checked

2026-10-25 against the Apache Flink 2.3.0 documentation (release-2.3 branch on GitHub). Confirmed from the back pressure monitoring page, the metrics reference (`inPoolUsage`, `outPoolUsage`, the three time metrics) and the generated configuration tables (`execution.checkpointing.unaligned.enabled`, `taskmanager.network.memory.buffer-debloat.enabled`, `taskmanager.memory.network.fraction`). Corrected the unaligned-checkpoint key and the UI colour meaning (red is busy, black is back pressured); removed unconfirmed version gates and the skew ratio.

Method: documentation only; no commands were run.

## Verify
- [ ] Identified bottleneck operator confirmed via `busyTimeMsPerSecond` metric, not just the UI's red/green indicator.
- [ ] Per-subtask `numRecordsIn` checked for skew before scaling parallelism.
- [ ] Checkpoint duration recovers to baseline after the fix (a real fix, not just hiding backpressure elsewhere).
- [ ] Async I/O capacity (`unorderedWait` buffer size) tuned to match downstream concurrency limits — not set so high it overwhelms the external system.
