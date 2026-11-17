---
id: computing-software.data-engineering.apache-spark.fetch-failures-and-lost-executors
name: fetch-failures-and-lost-executors
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, fetchfailedexception, executor-lost, shuffle-fetch, metadatafetchfailedexception, container-killed, stage-retry, spark-monitoring]
level: advanced
status: docs-checked
description: "Diagnose Spark FetchFailedException, ExecutorLostFailure and stage retries: find the real cause (OOM kill, spot loss, network) and fix memory, shuffle service or partitioning."
sources:
  - https://spark.apache.org/docs/latest/configuration.html#shuffle-behavior
  - https://spark.apache.org/docs/latest/monitoring.html
  - https://spark.apache.org/docs/latest/job-scheduling.html#dynamic-resource-allocation
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Fetch failures and lost executors

**Goal:** stop the loop of "FetchFailed -> resubmit parent stage -> fail again", by fixing why the shuffle data became unreachable.

## Read the symptom
- `FetchFailedException`: reducer could not get map output; the executor that held it died or was unreachable.
- Executor lost with a container kill for exceeding memory limits: memory kill.
- Heartbeat timeout (`spark.executor.heartbeatInterval` default 10s, must be well below `spark.network.timeout`, default 120s): long GC pauses or network partition.

FetchFailed is almost always secondary. Find the first executor loss in the driver log and the Executors tab (dead executors and their removal reason).

## Causes and fixes
| Root cause | Fix |
|---|---|
| Executor OOM/killed (container memory limit exceeded) | raise `spark.executor.memoryOverhead`; fewer cores per executor; more shuffle partitions to shrink per-task data |
| Spot/preemptible loss | enable decommissioning (`spark.decommission.enabled`, default false, plus `spark.storage.decommission.enabled`, default false, and `spark.storage.decommission.shuffleBlocks.enabled`, default true); external shuffle service; use on-demand for driver and core nodes |
| Dynamic allocation removed executor holding shuffle | `spark.shuffle.service.enabled=true` (external shuffle service, default false, must be set up) or `spark.dynamicAllocation.shuffleTracking.enabled` (default true; keeps executors holding shuffle data alive without the service) |
| Huge shuffle blocks (slow fetch) | increase `spark.sql.shuffle.partitions` (default 200) or rely on AQE; fix skew |
| Network flakiness / overloaded shuffle server | raise `spark.shuffle.io.maxRetries` (default 3) and `spark.shuffle.io.retryWait` (default 5s; maximum retry delay is maxRetries * retryWait); if needed raise `spark.network.timeout` |
| Long GC pauses -> heartbeat timeout | smaller heaps per executor, G1GC, cut cached data |
| Disk full on local dirs | bigger/more `spark.local.dir` volumes (overridden by `SPARK_LOCAL_DIRS` on standalone and `LOCAL_DIRS` on YARN); check for no-space-left errors |

## Where to look
Search the executor container logs (YARN or Kubernetes) for out-of-memory kills and no-space-left errors, and check the executor pod's last termination reason on Kubernetes.
Spark UI: Stages -> failed stage -> task "Errors" column; Executors -> dead executors, "Shuffle Write" sizes; SQL tab -> which exchange produced huge partitions.

## Limits
`spark.stage.maxConsecutiveAttempts` (default 4) is the number of consecutive stage attempts allowed before a stage is aborted. Raising it hides the problem.

## Verify
- [ ] No `Dead` executors with OOM reasons after the fix.
- [ ] Stage shows attempt 0 only; total task retries near zero.

## Checked

- Date: 2026-11-02.
- Confirmed against: Spark configuration page (defaults of spark.executor.heartbeatInterval 10s, spark.network.timeout 120s, spark.storage.decommission.enabled false, spark.shuffle.service.enabled false, spark.dynamicAllocation.shuffleTracking.enabled true, spark.sql.shuffle.partitions 200, spark.shuffle.io.maxRetries 3, spark.shuffle.io.retryWait 5s and the maxRetries x retryWait delay, spark.stage.maxConsecutiveAttempts 4, spark.local.dir overridden by SPARK_LOCAL_DIRS / LOCAL_DIRS, FetchFailedException retries the previous stage).
- Removed: MetadataFetchFailedException bullet, the exit-137 and "Remove reason" wording, and the yarn/kubectl command block (not stated in the fetched pages).

Method: documentation only; no commands were run.
