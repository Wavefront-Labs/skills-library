---
id: computing-software.data-engineering.apache-spark.reading-the-sql-tab
name: reading-the-sql-tab
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark-ui, sql-tab-metrics, query-plan, spark-sql, aqe, spark-monitoring]
level: advanced
status: docs-checked
description: "Read the Spark UI SQL/DataFrame tab: per-operator metrics in the plan graph, rows and bytes at each node, AQE plan changes, and spotting exploding joins or spills."
sources:
  - https://spark.apache.org/docs/latest/web-ui.html#sql-tab
  - https://spark.apache.org/docs/latest/sql-performance-tuning.html#adaptive-query-execution
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading the SQL tab

The SQL / DataFrame tab is the best place to see **which operator** is slow, because it maps metrics onto the physical plan rather than onto stages.

## Workflow
1. Open the query (by description or job id). Note total duration and the jobs it spawned.
2. Expand the plan graph. Each node shows metrics; WholeStageCodegen boxes show `duration` (total time across tasks, as min/med/max).
3. Follow row counts top to bottom:
   - Scan node: its file-count, size and `number of output rows` metrics. Compare files read vs files in the table to see if pruning worked.
   - `Filter`: output rows vs input; low selectivity after a scan means pushdown did not happen.
   - `Exchange` (shuffle): shuffle bytes and records written, with min/med/max per partition. Large max vs median = skew.
   - `SortMergeJoin`/`BroadcastHashJoin`: output rows. Output much larger than both inputs = exploding join (duplicate keys); check join keys.
   - `Sort`: `spill size` and `peak memory`. Non-zero spill means memory pressure.
   - `HashAggregate`: `spill size` and the fallback-to-sort task count (hash map too big).
4. With adaptive query execution (AQE) the plan is re-optimised at runtime: look for coalesced or skewed shuffle reads and joins changed to broadcast. Metric and node names vary by Spark version, so read them off your own UI.
5. Click a node's stage link to drill into task-level distribution in the Stages tab.

## Common readings
| Seen | Meaning | Action |
|---|---|---|
| Scan reads all files despite filter | no partition/predicate pushdown | filter on partition col, fix types, check DPP |
| Exchange partition max >> median | skew | AQE skew join, salting |
| Join output rows >> inputs | many-to-many keys | dedupe dimension, fix keys |
| Sort/Agg spill | not enough execution memory | more partitions, bigger executors |
| BatchEvalPython node slow | Python UDF bottleneck | built-ins or pandas UDF |

## Verify
- [ ] After a fix, the same node's metric (spill, rows, files read) changes as intended, not just total time.

## Checked

2026-10-28. Confirmed: the Spark web UI and performance-tuning pages cover the SQL tab and AQE. Removed: exact scan/exchange/aggregate metric names and AQE node names that the pages do not list.

Method: documentation only; no commands were run.
