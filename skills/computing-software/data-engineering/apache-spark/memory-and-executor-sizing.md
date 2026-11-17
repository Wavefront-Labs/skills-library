---
id: computing-software.data-engineering.apache-spark.memory-and-executor-sizing
name: memory-and-executor-sizing
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, executor-memory, spark-oom, memory-overhead, unified-memory-manager, spill-to-disk, garbage-collection, dynamic-allocation, spark-tuning, executor-cores, off-heap-memory, g1gc]
level: practitioner
status: docs-checked
description: "Size Spark executors, cores and memory correctly, and diagnose OOMs, spilling and GC pressure."   # quoted: YAML would cut an unquoted value at " #" or choke on ": "
sources:
  - https://spark.apache.org/docs/latest/tuning.html#memory-management-overview
  - https://spark.apache.org/docs/latest/configuration.html#memory-management
  - https://spark.apache.org/docs/latest/configuration.html#dynamic-allocation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spark executor and memory sizing

**Goal:** stop guessing executor shapes, and tell real OOM/spill root causes apart from "just add more memory."

## 1. The unified memory model
`spark.executor.memory` (minus 300MB) is split, by `spark.memory.fraction` (default 0.6), into the **unified region**, shared dynamically between **execution memory** (shuffles, joins, sorts, aggregations) and **storage memory** (cached RDDs/DataFrames) with `spark.memory.storageFraction` (default 0.5 of that region) as the eviction-immune storage share. Execution may evict storage only until storage falls to the protected region `R` (`spark.memory.storageFraction` of the unified region); storage cannot evict execution — a cache that keeps getting evicted mid-job usually means execution memory is starved, not that caching is broken.
- `spark.executor.memoryOverhead` (default `executorMemory * spark.executor.memoryOverheadFactor`, with a minimum of `spark.executor.minMemoryOverhead`; supported on YARN and Kubernetes) covers VM overheads, interned strings and other native overheads, plus PySpark executor memory when `spark.executor.pyspark.memory` is not set. **PySpark jobs need the overhead sized for the Python worker memory** — a container kill by the cluster manager with no on-heap OOM in the Spark UI points at overhead rather than `spark.executor.memory`.

## 2. Executor shape: wide-and-shallow vs narrow-and-deep
- Tasks running concurrently in one executor share its JVM heap, so more cores per executor means more tasks competing for the same execution memory and GC.
- Many small executors raise per-executor overhead; very large ones make one executor loss or long GC pause cost more. Pick a shape by measuring, not by a fixed core count.
- Size `spark.executor.memory` so `memory + memoryOverhead` fits the container the cluster manager grants, leaving room for the node's own daemons.

## 3. Reading spill and GC signals correctly
- **Spill (memory) / spill (disk)** metrics in the Spark UI's stage detail mean execution memory ran out mid-shuffle/sort and wrote intermediate data to local disk — not an error, but a major slowdown; the fix is usually fixing skew or widening `spark.sql.shuffle.partitions` (so each task handles less data), not blindly raising memory.
- A task failing with `java.lang.OutOfMemoryError: Java heap space` after long spill activity, vs. one OOMing instantly on a single huge partition (skew/broadcast-too-large), are different root causes — the Spark UI's event timeline plus "shuffle read size" per task tells you which; don't apply the same fix to both.
- High GC time (visible per-task in the UI, or via `-XX:+PrintGCDetails` on the executor JVM) with low spill usually means too many small objects (often from UDFs creating objects per-row, or an undersized unified memory region thrashing). Since Spark 4.0.0 the default JDK is 17, which makes G1GC the default collector; with large heaps the tuning guide suggests raising the G1 region size (`-XX:G1HeapRegionSize`). Reduce per-row object churn before adding memory.

## 4. Dynamic allocation
`spark.dynamicAllocation.enabled=true` lets the driver request/release executors based on pending task backlog — essential for shared clusters and ad hoc workloads, but set `minExecutors`/`maxExecutors` deliberately: unbounded max on a shared YARN/k8s cluster is how one job starves every other job's queue. Needs one of: the external shuffle service, `spark.dynamicAllocation.shuffleTracking.enabled`, or shuffle-block decommissioning, so releasing an executor does not lose shuffle data another stage still needs.

## Verify
- [ ] `memoryOverhead` was explicitly raised (not left at default) for any PySpark/Pandas-UDF/Arrow-heavy job before concluding `executor.memory` is the bottleneck.
- [ ] Spill size per stage checked in the Spark UI before increasing memory blindly — skew/partition-count fixes tried first.
- [ ] `dynamicAllocation.maxExecutors` is bounded to a value the shared cluster can actually give this job without starving others.

## Checked
Checked 2026-10-25 against the Apache Spark documentation sources (apache/spark docs/ and SQLConf.scala on master, last commit 2026-10-24; docs site: spark.apache.org/docs/latest).
Confirmed in tuning.md and configuration.md: unified region and R semantics (execution may evict storage down to R, not vice versa), spark.memory.fraction 0.6 of heap minus 300MB, spark.memory.storageFraction 0.5, memoryOverhead formula (factor times executor memory with a minimum, YARN and Kubernetes only, includes PySpark memory), G1GC default since JDK 17 / Spark 4.0.0, the three shuffle-data options for dynamic allocation. Removed the unsourced '4-5 cores' rule and HDFS-throughput claim.

Method: documentation only; no commands were run.
