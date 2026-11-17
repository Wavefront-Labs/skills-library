---
id: computing-software.data-engineering.apache-spark.spark-on-yarn
name: spark-on-yarn
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, spark-on-yarn, yarn, hadoop, emr, dataproc, yarn-queues, memory-overhead, yarn-logs, cluster-manager]
level: practitioner
status: docs-checked
description: "Run Spark on YARN (EMR, Dataproc, Hadoop): container sizing vs yarn limits, memoryOverhead, queues, the external shuffle service, and getting logs with yarn logs."
sources:
  - https://spark.apache.org/docs/latest/running-on-yarn.html
  - https://spark.apache.org/docs/latest/configuration.html#memory-management
  - https://github.com/apache/hadoop/blob/trunk/hadoop-yarn-project/hadoop-yarn/hadoop-yarn-common/src/main/resources/yarn-default.xml
  - https://github.com/apache/hadoop/blob/trunk/hadoop-yarn-project/hadoop-yarn/hadoop-yarn-site/src/site/markdown/CapacityScheduler.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spark on YARN

**Goal:** get executors that actually fit YARN containers, land in the right queue, and debug failed apps from YARN logs.

## Container sizing arithmetic
The YARN container for an executor is `spark.executor.memory` plus `spark.executor.memoryOverhead` (`executorMemory * spark.executor.memoryOverheadFactor`, with a minimum of `spark.executor.minMemoryOverhead`) plus `spark.executor.pyspark.memory` if set, and off-heap memory if enabled. The request must fit within YARN's `yarn.scheduler.maximum-allocation-mb`, and a node's containers within `yarn.nodemanager.resource.memory-mb` (both are Hadoop settings, see yarn-default.xml).

Worked example (illustrative numbers): a NodeManager offers 56 GB. Three containers of 16g heap + 2g overhead = 54 GB fit; three of 20g + 2g = 66 GB do not, so only two fit.

PySpark: executor memory used by Python workers counts toward the overhead unless `spark.executor.pyspark.memory` is set. A container killed by YARN for exceeding memory limits points at overhead rather than heap.

## Queues
```bash
spark-submit --master yarn --deploy-mode cluster --queue etl ...
```
Capacity/Fair scheduler queues cap resources per team. With the Capacity Scheduler, an application stays in `ACCEPTED` until there is room: one check is `maximum-am-resource-percent`, which limits the share of resources used by ApplicationMasters (default 10%). The queue can also be set with `spark.yarn.queue`.

## Dynamic allocation on YARN
```properties
spark.dynamicAllocation.enabled=true
spark.shuffle.service.enabled=true          # needs the spark_shuffle aux-service in yarn-site.xml (YarnShuffleService) on every NodeManager
spark.dynamicAllocation.minExecutors=2
spark.dynamicAllocation.maxExecutors=50
```
Setup (per the YARN guide): add `spark_shuffle` to `yarn.nodemanager.aux-services`, set `yarn.nodemanager.aux-services.spark_shuffle.class` to `org.apache.spark.network.yarn.YarnShuffleService`, and restart the NodeManagers. Alternatives to the shuffle service: `spark.dynamicAllocation.shuffleTracking.enabled=true` or shuffle-block decommissioning.

## Logs and status
```bash
yarn application -status <appId>
yarn logs -applicationId <appId> > app.log          # needs log aggregation (yarn.log-aggregation-enable)
yarn application -kill <appId>
```
In cluster mode the driver runs inside the ApplicationMaster, so its logs are in the AM container's logs.

## Gotchas
- If neither `spark.yarn.archive` nor `spark.yarn.jars` is set, Spark zips all jars under `$SPARK_HOME/jars` and uploads them to the distributed cache on each submit; set one of them to avoid that.
- In client mode the ApplicationMaster's memory is `spark.yarn.am.memory` (default 512m); in cluster mode use `spark.driver.memory`.
- `spark.yarn.executor.nodeLabelExpression` restricts the nodes executors run on.

## Verify
- [ ] The ResourceManager shows the app in the intended queue with all requested containers allocated.
- [ ] No memory-limit kills in `yarn logs` output.
- [ ] Executors per node x container size <= NodeManager memory.

## Checked
Checked 2026-10-25 against the Apache Spark documentation sources (apache/spark docs/ and SQLConf.scala on master, last commit 2026-10-24; docs site: spark.apache.org/docs/latest).
Confirmed in running-on-yarn.md: aux-service spark_shuffle setup, spark.yarn.am.memory 512m, spark.yarn.archive/jars upload behaviour, spark.yarn.queue, nodeLabelExpression, yarn logs with log aggregation. Confirmed in Hadoop yarn-default.xml (apache/hadoop trunk): yarn.scheduler.maximum-allocation-mb and yarn.nodemanager.resource.memory-mb exist; Hadoop CapacityScheduler.md: maximum-am-resource-percent (default 10%) and the ACCEPTED state. Removed EMR/Dataproc claims, unconfirmed preemption advice, a yarn list command and the 4g overhead figure.

Method: documentation only; no commands were run.
