---
id: computing-software.data-engineering.apache-spark.reading-the-spark-ui
name: reading-the-spark-ui
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, spark-ui, spark-ui-tabs, spark-monitoring, stages-tab, sql-tab, executors-tab, task-metrics, shuffle-read, gc-time, stragglers, spill]
level: practitioner
status: docs-checked
description: "Diagnose Spark jobs from the web UI: which tab answers which question, reading stage summary metrics (median vs max), SQL plan node metrics, spill, GC and executor health."
sources:
  - https://spark.apache.org/docs/latest/web-ui.html
  - https://spark.apache.org/docs/latest/monitoring.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading the Spark UI

**Goal:** go from "the job is slow/failed" to a specific cause (skew, spill, too few tasks, GC, a bad join) in minutes.

UI is at `http://<driver>:4040` while running (the port is `spark.ui.port`); after completion use the history server.

## Which tab answers what
| Question | Tab |
|---|---|
| Which part of my code is slow? | **SQL / DataFrame**: per-query plan graph with metrics per node |
| Is one task much slower than others? | **Stages** -> stage detail -> Summary Metrics |
| Are executors healthy / dying / GC-bound? | **Executors** |
| What config actually applied? | **Environment** |
| What is cached? | **Storage** |
| Streaming throughput | **Structured Streaming** |

## Stage detail: the summary metrics table
Look at Min / 25th / Median / 75th / Max for Duration, GC time, Shuffle Read Size, Spill (memory/disk), Input Size.
- **Max >> median** with Shuffle Read Size max >> median = **data skew** on the shuffle key.
- Same durations but max input larger = uneven input files.
- **Spill (disk) > 0** = partitions too large for execution memory: more shuffle partitions or more memory per core.
- **High GC time relative to task time** = memory pressure or huge objects (collect_list, wide rows).
- **Scheduler delay and task deserialization time** are listed in the summary metrics; check them when tasks are tiny.
- Task count: 1 task on a big stage = something forced a single partition.

Event timeline (enable on the stage page) shows whether tasks run in parallel waves or the stage waits on one straggler.

## SQL tab
Click a query -> graph of physical operators with metrics:
- Scan nodes: files and bytes read -> is pruning working?
- `Exchange`: shuffle bytes written: the most expensive edges.
- Join nodes and `BroadcastExchange`: join strategy and its cost.
- AQE shuffle-read nodes: whether AQE coalesced or split skewed partitions.
- Row counts at each node: spot join explosions (output rows >> input rows).

## Executors tab
The Executors tab lists every allocated executor with links to its logs (stderr holds the real exception). Look for failed tasks and executors that disappeared.

## Failed jobs
Failed stages show a failure reason on the Stages tab; read down to the first `Caused by`. If shuffle fetches fail, look for the executor that died first.

## Verify
- [ ] For a slow job you can name the slowest stage, its operator in the SQL tab, and whether the cause is skew, spill, GC or parallelism.
- [ ] After a fix, the same metrics (max vs median, spill) show the improvement.

## Checked

2026-10-28. Confirmed against: Spark web UI page (tabs: Jobs, Stages, Storage, Environment, Executors, SQL, Structured Streaming; summary metrics incl. scheduler delay; executor log links; failed stages show failure reason), configuration page (spark.ui.port 4040). Removed (not confirmable in the fetched pages): port-increment note, 40 min vs 20 s example, GC 10% threshold, plan node names SortMergeJoin/AQEShuffleRead/Scan parquet, FetchFailedException interpretation, Executors tab metric list.

Method: documentation only; no commands were run.
