---
id: computing-software.data-engineering.apache-spark.gpu-and-resource-profiles
name: gpu-and-resource-profiles
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, spark-gpu-scheduling, resource-profiles, stage-level-scheduling, gpu, rapids, discovery-script, spark-architecture]
level: advanced
status: docs-checked
description: "Schedule GPUs and custom resources in Spark: executor/task resource amounts, discovery scripts, and stage-level ResourceProfiles that give one stage different executors."
sources:
  - https://spark.apache.org/docs/latest/configuration.html#custom-resource-scheduling-and-configuration-overview
  - https://spark.apache.org/docs/latest/job-scheduling.html#stage-level-scheduling-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GPU and custom resource scheduling

**Use when:** some or all of a Spark job needs GPUs (or FPGAs or another countable resource).

## Static: every executor gets GPUs
```bash
spark-submit \
  --conf spark.executor.resource.gpu.amount=1 \
  --conf spark.task.resource.gpu.amount=0.25 \
  --conf spark.executor.resource.gpu.discoveryScript=<PATH_TO_DISCOVERY_SCRIPT> ...
```
- Resources are configured per resource name: `spark.executor.resource.{resourceName}.amount`, `spark.task.resource.{resourceName}.amount` and `spark.executor.resource.{resourceName}.discoveryScript`; read the custom-resource section of the configuration page for the full list, including the driver settings and cluster-manager notes.

## Stage-level scheduling (ResourceProfile)
ETL on CPU executors, training on GPU executors, in the same app:
Build a ResourceProfile with `ResourceProfileBuilder` (executor and task resource requests) and apply it to an RDD with `RDD.withResources`; signatures are in the PySpark API docs.
- `spark.scheduler.resource.profileMergeConflicts` (default false) makes Spark merge ResourceProfiles when different profiles meet in one stage; otherwise it throws.
- The job scheduling page's stage-level scheduling section lists the dynamic-allocation requirements.

## SQL on GPU
The RAPIDS Accelerator for Apache Spark has its own documentation; this skill covers only Spark's own resource scheduling.

## Verify
- [ ] The Spark UI shows executors with the expected resources.
- [ ] Each task uses a distinct GPU.
- [ ] With a ResourceProfile, new executors appear for that stage.

## Checked

2026-10-28. Confirmed against: Spark configuration page (custom resource scheduling: spark.executor/task/driver.resource.{resourceName}.* , discoveryScript, stage-level scheduling, RDD.withResources, ResourceProfileBuilder, spark.scheduler.resource.profileMergeConflicts). Removed (not confirmable in the fetched pages): discovery script path and JSON format, vendor setting, TaskContext resources call, executor/task core arithmetic, ResourceProfile code (builder method names), TaskResourceProfile claim, dynamic-allocation requirement wording, RAPIDS plugin settings, nvidia-smi.

Method: documentation only; no commands were run.
