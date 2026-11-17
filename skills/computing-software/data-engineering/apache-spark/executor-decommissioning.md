---
id: computing-software.data-engineering.apache-spark.executor-decommissioning
name: executor-decommissioning
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, executor-decommissioning, spot-instances, preemption, shuffle-migration, rdd-migration, kubernetes, graceful-shutdown]
level: advanced
status: docs-checked
description: "Enable graceful executor decommissioning in Spark 3.1+ so spot/preemptible node loss and scale-down migrate shuffle and cached blocks instead of recomputing stages."
sources:
  - https://spark.apache.org/docs/latest/configuration.html#spark-properties
  - https://spark.apache.org/docs/latest/running-on-kubernetes.html
  - https://spark.apache.org/docs/latest/spark-standalone.html
  - https://issues.apache.org/jira/browse/SPARK-20624
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Graceful executor decommissioning

**Goal:** when an executor is going away (spot reclaim, autoscaler scale-down, k8s pod eviction), move its shuffle files and cached blocks to peers so the job does not fail stages and recompute.

## Settings
```properties
spark.decommission.enabled=true                      # default false
spark.storage.decommission.enabled=true
spark.storage.decommission.shuffleBlocks.enabled=true
spark.storage.decommission.rddBlocks.enabled=true
# optional: copy to object storage when no peer has room
spark.storage.decommission.fallbackStorage.path=s3a://bucket/spark-fallback/
# duration after which Spark forces a decommissioning executor to exit (default none; keep it high so block migration can finish)
spark.executor.decommission.forceKillTimeout=120s
```
With dynamic allocation on k8s (no external shuffle service) also set:
```properties
spark.dynamicAllocation.enabled=true
spark.dynamicAllocation.shuffleTracking.enabled=true
```
With `spark.decommission.enabled`, Spark decommissions an executor instead of killing it when dynamic allocation releases it. Dynamic allocation also accepts shuffle-block decommissioning (`spark.decommission.enabled` plus `spark.storage.decommission.shuffleBlocks.enabled`) as an alternative to shuffle tracking.

## Triggers
- **Signal:** `spark.executor.decommission.signal` (default `PWR`) is the signal that triggers an executor to start decommissioning.
- **Kubernetes:** `spark.kubernetes.decommission.script` (default `/opt/decom.sh`) is the script used for graceful decommissioning; `spark.kubernetes.executor.decommissionLabel` labels pods that are exiting.
- **Standalone:** `sbin/decommission-worker.sh` gracefully decommissions a worker, letting in-progress tasks finish and migrating shuffles before it exits.
- `spark.executor.decommission.killInterval` (default none) is the duration after which an outside, non-Spark service kills a decommissioned executor.

## What to expect
Spark tries to migrate RDD blocks and shuffle blocks from the decommissioning executor to a remote executor (or to fallback storage when configured).

## Gotchas
- Large shuffle outputs may not finish migrating before the executor is killed; keep `forceKillTimeout` high (low values prevent block migration from completing) or use fallback storage.
- The fallback storage location is not cleaned up by Spark; manage it with a TTL (lifecycle) policy.
- RDD block migration adds network traffic during scale-down; set `spark.storage.decommission.rddBlocks.enabled=false` if cached data is not worth moving.

## Verify
- [ ] Force a scale-down mid-job and confirm the application does not recompute lost shuffle stages.
- [ ] No stage retries in the Spark UI after the executor leaves.

## Checked
Checked 2026-10-25 against the Apache Spark documentation sources (apache/spark docs/ and SQLConf.scala on master, last commit 2026-10-24; docs site: spark.apache.org/docs/latest).
Confirmed in configuration.md, running-on-kubernetes.md, spark-standalone.md and job-scheduling.md: spark.decommission.enabled (default false), storage.decommission.* flags and fallbackStorage.path (not cleaned up by Spark), executor.decommission.killInterval (none, outside service) vs forceKillTimeout (Spark forces exit; should be high), executor.decommission.signal default PWR, kubernetes.decommission.script default /opt/decom.sh, sbin/decommission-worker.sh, shuffle-data options for dynamic allocation. Wrong claims fixed: killInterval is not Spark's own timeout; kill -PWR on a worker and YARN rmadmin were unconfirmed and removed. Removed cloud-vendor notice timings and unconfirmed log lines.

Method: documentation only; no commands were run.
