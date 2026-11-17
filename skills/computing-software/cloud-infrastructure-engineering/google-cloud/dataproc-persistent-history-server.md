---
id: computing-software.cloud-infrastructure-engineering.google-cloud.dataproc-persistent-history-server
name: dataproc-persistent-history-server
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, dataproc, persistent-history-server, phs, spark-history, ephemeral-clusters]
level: practitioner
status: docs-checked
description: "Keep Spark and MapReduce history after ephemeral Dataproc clusters and Serverless batches are deleted: write logs to Cloud Storage and run a Persistent History Server."
sources: ["https://docs.cloud.google.com/managed-spark/docs/concepts/jobs/history-server", "https://docs.cloud.google.com/sdk/gcloud/reference/dataproc/batches/submit/spark"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dataproc Persistent History Server

Ephemeral clusters lose their Spark UI when deleted. A PHS is a small single-node cluster that reads
event logs from Cloud Storage written by many job clusters.

## 1. Create the PHS
```bash
gcloud dataproc clusters create phs --region=<R> --single-node --enable-component-gateway \
  --properties='spark:spark.history.fs.logDirectory=gs://<B>/*/spark-job-history,mapred:mapreduce.jobhistory.read-only.dir-pattern=gs://<B>/*/mapreduce-job-history/done,spark:spark.history.custom.executor.log.url.applyIncompleteApplication=false'
```
The wildcard lets one PHS read logs from many clusters' folders. On 2.0+ image clusters the page also requires `spark.history.custom.executor.log.url` (a literal value with `{{PLACEHOLDERS}}`, copy it from the History Server page) alongside `applyIncompleteApplication=false`.

## 2. Point job clusters at the bucket
```bash
gcloud dataproc clusters create etl-$(date +%s) --region=<R> \
  --properties='spark:spark.history.fs.logDirectory=gs://<B>/etl/spark-job-history,spark:spark.eventLog.dir=gs://<B>/etl/spark-job-history,mapred:mapreduce.jobhistory.done-dir=gs://<B>/etl/mapreduce-job-history/done,mapred:mapreduce.jobhistory.intermediate-done-dir=gs://<B>/etl/mapreduce-job-history/intermediate-done'
```
Serverless batches: `gcloud dataproc batches submit ... --history-server-cluster=projects/<P>/regions/<R>/clusters/phs`.

## 3. Open it
Open the Component Gateway web interfaces of the `phs` cluster (enabled by `--enable-component-gateway`).

## Gotchas
- The PHS and the job clusters should be in the same project, and the PHS image version must match the job clusters' image version (use `--image-version` on the PHS).
- If `spark.history.fs.logDirectory` and `spark.eventLog.dir` are both set, they must point to directories in the same bucket; the same applies to the two MapReduce done-dir properties.
- By default, job history is written to the cluster temp bucket (`/spark-job-history`, `/mapreduce-job-history/done`); set the properties above to put it somewhere durable and shared.

## Checked
2026-10-31. Confirmed against the Dataproc (Managed Service for Apache Spark) Persistent History Server page (single-node PHS, `--enable-component-gateway`, wildcard bucket paths, Spark, MapReduce properties, 2.0+ extra properties, same-bucket rule, image version must match, default temp-bucket locations) and the `gcloud dataproc batches submit spark` reference (`--history-server-cluster`). Removed unconfirmed: objectViewer role, 30-day lifecycle, rolling event log advice, console menu path, and corrected the image-version rule (must match, not same or newer).
Method: documentation only; no commands were run.

## Verify
- [ ] After deleting a job cluster, its applications still appear and open in the PHS Spark UI.
