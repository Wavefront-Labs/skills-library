---
id: computing-software.data-engineering.apache-spark.speculative-execution
name: speculative-execution
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, speculative-execution, spark-speculation, stragglers, slow-nodes, idempotent-writes, task-retries]
level: practitioner
status: docs-checked
description: "Use spark.speculation to re-launch straggler tasks on other executors: thresholds, when it helps vs hides skew, and why sinks must be idempotent."
sources:
  - https://spark.apache.org/docs/latest/configuration.html#scheduling
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Speculative execution

**Goal:** cut tail latency caused by a bad node (noisy neighbour, failing disk, throttled VM) by running a duplicate copy of slow tasks and taking whichever finishes first.

## Settings
```properties
spark.speculation=true                   # default false
spark.speculation.interval=100ms         # how often to check
spark.speculation.multiplier=3           # default 3: how many times slower than the median counts as slow
spark.speculation.quantile=0.9           # only after 90% of tasks in the stage finished
spark.speculation.minTaskRuntime=100ms   # minimum runtime before a task is considered (default)
# Spark 3.2+: speculate in stages with few tasks (no default)
spark.speculation.task.duration.threshold=10min
# Spark 3.4+, default true: only speculate tasks whose data process rate or duration is inefficient
spark.speculation.efficiency.enabled=true
```

## When it helps
- Same work per task, but one executor/host is slow. In the Spark UI Stages tab, the slow tasks cluster on one host and have similar input size to fast ones.

## When it does not
- **Data skew**: the slow task has 50x the input records. A speculative copy reads the same skewed partition and is just as slow while burning resources. Fix with AQE skew join or salting.

Check in the UI: the stage task table has Input Size / Records columns to compare slow and fast tasks.

## Correctness requirement
Two attempts of one task may run concurrently. Safe when output goes through Spark's commit protocol (files via committer, Delta/Iceberg). Unsafe when tasks have side effects:
- `foreach` / `foreachPartition` writing to an external DB or calling an API -> duplicate writes.
- JDBC sink append mode without an upsert key -> duplicate rows.
Turn speculation off for those jobs, or make writes idempotent (upsert on a natural key).

## Gotchas
- `spark.speculation` is off by default. Check the Environment tab for the value your application started with.
- Speculative tasks inside `foreachBatch` with non-idempotent writes duplicate data.

## Verify
- [ ] Stage tail latency (max vs 75th percentile task time) drops after enabling.
- [ ] No duplicate rows in side-effecting sinks; jobs with external writes have speculation disabled.

## Checked
Checked 2026-10-25 against the Apache Spark documentation sources (apache/spark docs/ and SQLConf.scala on master, last commit 2026-10-24; docs site: spark.apache.org/docs/latest).
Confirmed in configuration.md: spark.speculation default false, interval 100ms, quantile 0.9, minTaskRuntime 100ms, task.duration.threshold (since 3.2.0, no default, for stages with few tasks), efficiency.enabled (since 3.4.0, default true). Wrong claim fixed: spark.speculation.multiplier default is 3, not 1.5; efficiency.enabled was misdescribed. Removed unconfirmed UI marker text.

Method: documentation only; no commands were run.
