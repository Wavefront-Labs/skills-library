---
id: computing-software.data-engineering.apache-spark.fair-scheduler-pools
name: fair-scheduler-pools
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, fair-scheduler, scheduler-pools, spark-scheduler-mode, concurrent-jobs, fairscheduler-xml, shared-cluster, job-scheduling]
level: advanced
status: docs-checked
description: "Run concurrent jobs inside one Spark application fairly: spark.scheduler.mode=FAIR, pools in fairscheduler.xml, setLocalProperty per thread, weights and minShare."
sources:
  - https://spark.apache.org/docs/latest/job-scheduling.html#scheduling-within-an-application
  - https://spark.apache.org/docs/latest/configuration.html#scheduling
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fair scheduler pools within one Spark application

**Goal:** when one SparkSession runs several jobs at once (multiple threads, a shared notebook cluster, a streaming app plus batch side jobs), stop one big job from starving the others.

Default `spark.scheduler.mode=FIFO`: jobs in one SparkContext queue one after another. `FAIR` shares resources between jobs and supports pools.

## Configure
```properties
spark.scheduler.mode=FAIR
spark.scheduler.allocation.file=file:///opt/spark/conf/fairscheduler.xml   # local or HDFS path; or put fairscheduler.xml on the classpath
```
```xml
<?xml version="1.0"?>
<allocations>
  <pool name="interactive">
    <schedulingMode>FAIR</schedulingMode>
    <weight>3</weight>
    <minShare>8</minShare>      <!-- minimum CPU cores -->
  </pool>
  <pool name="batch">
    <schedulingMode>FIFO</schedulingMode>
    <weight>1</weight>
    <minShare>0</minShare>
  </pool>
</allocations>
```

## Assign jobs to pools (per thread)
```python
from concurrent.futures import ThreadPoolExecutor

def run(table, pool):
    sc = spark.sparkContext
    sc.setLocalProperty("spark.scheduler.pool", pool)   # thread-local
    spark.table(table).write.mode("overwrite").saveAsTable(table + "_copy")

with ThreadPoolExecutor(max_workers=4) as ex:
    for t in ["a", "b", "c", "d"]:
        ex.submit(run, t, "batch")
```

## Semantics
- Without intervention, jobs go to the default pool; each pool gets an equal share of the cluster and, inside a pool, jobs run FIFO unless `schedulingMode` is FAIR.
- Defaults: `weight` 1, `minShare` 0 (cores). Active pools' `minShare` is met first, then extra resources are split by `weight`.
- `setLocalProperty("spark.scheduler.pool", null)` clears a thread's pool.

## Gotchas
- This is scheduling inside ONE application; sharing between applications is the cluster manager's job.

## Verify
- [ ] Jobs launched from a thread with the pool property set run in that pool.
- [ ] Running a small interactive query while a large batch job runs completes in seconds, not after the batch job.

## Checked
Checked 2026-10-25 against the Apache Spark documentation sources (apache/spark docs/ and SQLConf.scala on master, last commit 2026-10-24; docs site: spark.apache.org/docs/latest).
Confirmed in job-scheduling.md and configuration.md: spark.scheduler.mode default FIFO, allocation file local/HDFS path or classpath fairscheduler.xml, per-thread spark.scheduler.pool local property and clearing with null, default pool behaviour, schedulingMode / weight (default 1) / minShare (default 0, CPU cores) semantics. Removed unconfirmed PySpark pinning, Databricks, streaming-pool and UI-table claims.

Method: documentation only; no commands were run.
