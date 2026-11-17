---
id: computing-software.data-engineering.apache-flink.rescaling-with-max-parallelism
name: rescaling-with-max-parallelism
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, state-backend, max-parallelism, key-groups, rescaling, savepoint, parallelism, stateful-upgrade]
level: advanced
status: docs-checked
description: "Rescale stateful Flink jobs safely: key groups and max parallelism, why it is fixed after first deploy, choosing a value, and rescaling via savepoint or adaptive scheduler."
sources:
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/execution/parallel/
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/production_ready/
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/elastic_scaling/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rescaling with max parallelism

**Goal:** be able to scale a stateful job up and down for years without losing state.

## Key groups
Keyed state is partitioned into **key groups**; their number equals the operator's **max parallelism**. Each parallel subtask owns a contiguous range of key groups. Rescaling reassigns ranges, so parallelism can be any value up to max parallelism.

Changing max parallelism changes key-to-key-group mapping: it is effectively fixed at first deployment, so do not change it on a job whose state you need to keep.

## Defaults
If unset, Flink derives it from the operator parallelism: 128 for parallelism up to 128, otherwise the next power of two of `parallelism + parallelism / 2`, capped at 2^15 (32768). A job first deployed with parallelism 4 gets 128, so you can never scale past 128.

## Set it explicitly
```java
env.setMaxParallelism(720);                         // job default
stream.keyBy(...).process(...).setMaxParallelism(720).uid("agg");
```
Choose a value with many divisors so common parallelism values get even key group counts, and leave headroom above the largest parallelism you expect.

## Rescale procedures
1. **Savepoint + restart** (any deployment):
```bash
flink stop --savepointPath s3://chk/savepoints/ <jobId>
flink run --fromSavepoint s3://chk/savepoints/savepoint-xxx --parallelism 24 job.jar
```
2. **Adaptive scheduler / reactive mode**: `jobmanager.scheduler: adaptive` at cluster level; parallelism follows available slots, bounded by max parallelism (at most 2^15). `jobmanager.adaptive-scheduler.scaling-interval.min` (default 30 s) limits how often it rescales.

## Things that block rescaling
- Max parallelism lower than desired parallelism.

## Verify
- [ ] Max parallelism explicitly set in the job and documented.
- [ ] Rescale test from savepoint at p=4 -> p=12 -> p=6 succeeds in staging with state intact.

## Checked
2026-10-31. Confirmed against the Flink stable Parallel Execution, Production Readiness Checklist, Elastic Scaling and CLI pages: default max-parallelism rule (128 floor, 2^15 cap), `jobmanager.scheduler: adaptive`, scaling-interval.min default 30 s, `flink stop --savepointPath`, `flink run --fromSavepoint --parallelism`. Removed: the config key `pipeline.max-parallelism`, the specific restore-error claim, divisor/overhead advice figures, operator `spec.job` fields, the union-state and `uid()` remarks and the Kafka/skew gotchas (not on these pages).
Method: documentation only; no commands were run.
