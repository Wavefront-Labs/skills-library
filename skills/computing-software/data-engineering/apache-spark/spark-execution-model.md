---
id: computing-software.data-engineering.apache-spark.spark-execution-model
name: spark-execution-model
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, spark-architecture, lazy-evaluation, narrow-vs-wide, driver-and-executors, spark-execution-model, jobs-stages-tasks, dag-scheduler, shuffle-boundary, task-slots, pyspark]
level: practitioner
status: docs-checked
description: "Reason about Spark's driver, executors, jobs, stages and tasks: where code runs, what creates a stage boundary, how many tasks run at once, and how to read it in the UI."
sources:
  - https://spark.apache.org/docs/latest/cluster-overview.html
  - https://spark.apache.org/docs/latest/rdd-programming-guide.html#shuffle-operations
  - https://spark.apache.org/docs/latest/web-ui.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spark execution model: driver, executors, jobs, stages, tasks

**Goal:** predict where each line of a Spark program runs and how much parallelism you get, so you can size clusters and debug "why is this slow / why did the driver die".

## The pieces
| Piece | What it is | Runs |
|---|---|---|
| Driver | The JVM running your `main`/notebook, holding the `SparkSession`, building plans, scheduling tasks | One per application |
| Cluster manager | Grants resources: standalone, YARN, Kubernetes | External |
| Executor | JVM process on a worker; runs tasks, caches data, serves shuffle files | Many per app |
| Task | One unit of work on one partition | One per core slot |

- **Parallelism ceiling = executors x `spark.executor.cores` / `spark.task.cpus`** (task slots). 10 executors x 4 cores = 40 tasks at once (default `spark.executor.cores` is 1 on YARN, all worker cores in standalone).
- `spark.task.cpus` (default 1) is the cores allocated per task: raising it reduces slots.

## Job -> stage -> task
- An **action** (`count`, `collect`, `write`, `show`, `toPandas`) triggers a **job**. Transformations are lazy.
- The DAG scheduler cuts a job into **stages at shuffle boundaries** (wide dependencies: `groupBy`, `join` without broadcast, `repartition`, `distinct`, window `partitionBy`). Narrow ops (`select`, `filter`, `withColumn`, `union`) pipeline inside one stage.
- Each stage has one task per partition of its input.
- Some "transformations" start jobs anyway: `spark.read.csv(..., inferSchema=True)` scans data, `df.cache().count()`, sort-range sampling for `orderBy`.

## Where code runs (the classic bugs)
- Code in the driver body runs once on the driver. Code inside a UDF/lambda runs on executors, serialised there.
- `collect()` / `toPandas()` pulls all rows to the driver -> driver OOM. Use `limit`, `take`, or write to storage.
- Accumulator updates inside transformations may be applied more than once if tasks or stages are re-executed; only updates inside actions are applied once.

## Reading it
```python
df = spark.read.parquet("s3://bucket/events/")      # job for schema/file listing only
agg = df.groupBy("country").count()                   # lazy
agg.explain("formatted")                              # Exchange = shuffle = stage boundary
agg.write.mode("overwrite").parquet("s3://bucket/out/")  # job with 2 stages
```
In the Spark UI: Jobs tab -> click job -> DAG visualisation shows stages split at `Exchange`; Stages tab shows task count, median vs max duration and shuffle read/write.

## Gotchas
- Too few partitions: slots sit idle. Too many tiny partitions: scheduling overhead and small files on write.
- `spark.driver.maxResultSize` (default 1g) aborts jobs whose collected results exceed it: fix the code, not the limit.

## Verify
- [ ] For a given job you can name each stage boundary from the `explain` output (count of `Exchange` nodes).
- [ ] Total task slots = executors x cores matches the "Active tasks" peak in the Executors tab.
- [ ] No `collect()`/`toPandas()` of unbounded data in production code.

## Checked

2026-11-01. Confirmed against the Spark configuration page (`spark.driver.maxResultSize` default 1g, `spark.task.cpus` default 1, `spark.executor.cores` defaults) and the RDD programming guide (stages separated by shuffles, shuffle-causing operations, accumulator semantics). Removed: Mesos note, wave arithmetic, AQE stage claim, UDF pickling/print notes, partition-size and driver-memory advice (not on the cited pages).

Method: documentation only; no commands were run.
