---
id: computing-software.data-engineering.apache-spark.caching-and-persistence
name: caching-and-persistence
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, spark-tuning, spark-caching, persist-storage-level, cache, unpersist, memory-and-disk, checkpoint, localcheckpoint, lineage-truncation, disk-cache]
level: practitioner
status: docs-checked
description: "Decide when to cache in Spark: reuse vs one-pass, storage levels, materialising the cache, unpersist, checkpoint to cut lineage, and why caching often makes jobs slower."
sources:
  - https://spark.apache.org/docs/latest/rdd-programming-guide.html#rdd-persistence
  - https://spark.apache.org/docs/latest/sql-performance-tuning.html#caching-data-in-memory
  - https://docs.databricks.com/en/optimizations/disk-cache.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Caching and persistence in Spark

**Goal:** cache only where it saves recomputation, and release it, so you do not trade a fast job for memory pressure and spills.

## When caching helps
- The same DataFrame is used by **two or more actions** (e.g. written to two sinks, or counted then written) and recomputing it is expensive (wide joins, remote JDBC reads, heavy UDFs).
- Iterative algorithms (ML training loops) reading the same input repeatedly.
- Interactive exploration on a stable subset.

## When it hurts
- Single-pass pipelines (read -> transform -> write once): caching adds a full materialisation for nothing.
- Caching the raw input before a selective filter: you pin all columns/rows in memory instead of letting Parquet pruning skip them. Cache after filters and projections.
- Huge datasets that do not fit: evictions and recomputation, or spills with `MEMORY_AND_DISK`.

## Doing it right
```python
from pyspark import StorageLevel
enriched = orders.join(customers, "customer_id").filter("status = 'paid'").select(...)
enriched.persist(StorageLevel.MEMORY_AND_DISK)   # DataFrame .cache() uses the default MEMORY_AND_DISK level
enriched.count()                                  # caching is lazy: an action materialises it
enriched.write.parquet(".../a")
enriched.groupBy("country").sum("amount").write.parquet(".../b")
enriched.unpersist()                              # free executors' storage memory
```
- `DISK_ONLY` for large reused intermediates when memory is tight; `MEMORY_ONLY` recomputes evicted partitions.
- SQL: `CACHE TABLE t AS SELECT ...`, `UNCACHE TABLE t`, `CLEAR CACHE`.
- The Storage tab of the Spark UI shows how much of each cached DataFrame is in memory and on disk.

## Checkpoint to cut lineage
Long iterative plans (loops of joins, hundreds of `withColumn`s) grow the logical plan until analysis itself takes minutes or the driver OOMs.
```python
spark.sparkContext.setCheckpointDir("s3://tmp/ckpt/")
df = df.checkpoint()        # eager: writes to reliable storage, new plan starts from the files
df = df.localCheckpoint()   # executor-local, faster, lost if an executor dies
```
Writing to Parquet and reading back achieves the same and is easier to inspect.

## Platform caches
- Databricks disk cache (formerly Delta cache) caches remote Parquet/Delta file data on local SSDs automatically on supported instance types; usually better than manual `.cache()` for scan-heavy repeated queries.
- Cached data reflects the moment of caching: if the source table changes, the cache is stale until unpersisted/refreshed.

## Verify
- [ ] Each `cache()`/`persist()` has a matching `unpersist()` and at least two consuming actions.
- [ ] Storage tab shows 100% cached for the intended DataFrame and nothing else lingering.
- [ ] Job wall time compared with and without the cache; keep it only if faster.

## Checked

2026-10-28. Confirmed: MEMORY_AND_DISK storage level on the Dataset API and RDD persistence pages. Removed: an unconfirmed serialization note and a UI column name.

Method: documentation only; no commands were run.
