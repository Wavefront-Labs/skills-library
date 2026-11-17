---
id: computing-software.cloud-infrastructure-engineering.google-cloud.dataproc-cluster-and-spark-properties
name: dataproc-cluster-and-spark-properties
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, dataproc, dataproc-cluster-properties, spark-properties, yarn, tuning]
level: advanced
status: gated
description: "Set Dataproc cluster properties with file prefixes (spark:, yarn:, dataproc:), job-time overrides, and the Spark memory, shuffle and dynamic allocation settings that matter."
sources: ["https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/cluster-properties", "https://cloud.google.com/dataproc/docs/support/spark-job-tuning", "https://spark.apache.org/docs/latest/configuration.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dataproc cluster and Spark properties

## 1. Prefixes at cluster creation
`--properties` uses `<file-prefix>:<property>=<value>`; Dataproc writes them into the config files.
```bash
gcloud dataproc clusters create etl --region=<R> \
  --properties='spark:spark.executor.cores=<N>,spark:spark.executor.memory=<MEM>,yarn:yarn.nodemanager.resource.memory-mb=<MB>,dataproc:efm.spark.shuffle=primary-worker'
```
| Prefix | File |
|---|---|
| `spark:` | Spark config |
| `yarn:` | YARN config |
| `hdfs:` | HDFS config |
| `dataproc:` | Dataproc service features such as EFM (`dataproc:efm.spark.shuffle`) |

The file each other prefix (`core:`, `hive:`, `mapred:`, `spark-env:`) maps to is (gated: unconfirmed, source is paywalled or blocked). Look up the full prefix table in the cluster properties page.

## 2. Job-level overrides
`gcloud dataproc jobs submit spark ... --properties=spark.sql.shuffle.partitions=<N>` (no prefix).

## 3. Settings that usually matter
- Executor sizing: leave room for `spark.executor.memoryOverhead` inside the YARN node memory (see the Dataproc Spark job tuning page).
- `spark.dynamicAllocation.enabled` is covered on the Spark job tuning page; cap executors on shared clusters.
- With secondary (preemptible) workers, enable **Enhanced Flexibility Mode** (`dataproc:efm.spark.shuffle=primary-worker`) so shuffle data survives preemption.

## Gotchas
- Verify effective values in the Spark UI Environment tab rather than trusting the command line.
- Setting executor memory above what YARN offers leaves executors pending forever.

## Verify
- [ ] Spark UI → Environment tab shows the effective values; YARN UI shows expected executors per node.

## Checked
2026-10-28. Confirmed on the Dataproc cluster properties page (`--properties` prefixes `spark:`, `hdfs:`, `dataproc:`, `dataproc:efm.spark.shuffle=primary-worker` for Enhanced Flexibility Mode) and the Spark job tuning page (`spark.executor.memoryOverhead`, `spark.dynamicAllocation.enabled`, `yarn:`).
Gated: the file mapping of the `core:`, `hive:`, `mapred:` and `spark-env:` prefixes.
Removed: example numeric sizing, cores-per-executor and 10% overhead guidance, adaptive/skew defaults, job-over-cluster precedence claim, silent-typo and Serverless claims, and the post-creation change rule.
Method: documentation only; no commands were run.
