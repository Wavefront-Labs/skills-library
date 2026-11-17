---
id: computing-software.cloud-infrastructure-engineering.google-cloud.submitting-dataproc-jobs-with-gcloud
name: submitting-dataproc-jobs-with-gcloud
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, dataproc, gcloud-dataproc-jobs, dataproc-job-submit, spark, pyspark]
level: practitioner
status: docs-checked
description: "Submit, track and kill Dataproc jobs with gcloud: PySpark, Spark JAR, Spark SQL and Hive jobs, dependencies, job properties, restartable jobs, labels, and driver output."
sources: ["https://cloud.google.com/dataproc/docs/guides/submit-job", "https://cloud.google.com/sdk/gcloud/reference/dataproc/jobs/submit", "https://cloud.google.com/dataproc/docs/concepts/jobs/restartable-jobs", "https://cloud.google.com/dataproc/docs/guides/dataproc-job-output"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Submitting Dataproc jobs with gcloud

## 1. Job types
```bash
# PySpark with deps
gcloud dataproc jobs submit pyspark gs://<B>/jobs/etl.py --cluster=etl --region=<R> \
  --py-files=gs://<B>/jobs/lib.zip --files=gs://<B>/conf/app.yaml \
  --jars=gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-<VERSION>.jar \
  --properties=spark.executor.memory=8g,spark.dynamicAllocation.maxExecutors=50 \
  --labels=pipeline=orders --id=orders-etl-$(date +%Y%m%d%H%M) \
  -- --date=2026-10-16

# Spark JAR
gcloud dataproc jobs submit spark --cluster=etl --region=<R> --class=com.acme.Main --jars=gs://<B>/app.jar -- arg1
# Spark SQL / Hive
gcloud dataproc jobs submit spark-sql --cluster=etl --region=<R> -f gs://<B>/sql/daily.sql --params=dt=2026-10-16
```
Args after `--` go to your program. `--id` makes resubmits idempotent (duplicate id is rejected).

## 2. Track and control
```bash
gcloud dataproc jobs list --region=<R> --cluster=etl --state-filter=active
gcloud dataproc jobs wait <JOB_ID> --region=<R>       # streams driver output
gcloud dataproc jobs kill <JOB_ID> --region=<R>
gcloud dataproc jobs describe <JOB_ID> --region=<R> --format='value(driverOutputResourceUri,status.state)'
```
Driver output lives in the cluster's staging bucket (`driverOutputResourceUri`); YARN logs via the
component gateway or Cloud Logging (`resource.type="cloud_dataproc_cluster"`).

## 3. Restartable jobs
`--max-failures-per-hour=3 --max-failures-total=10` restarts the driver on failure (streaming jobs,
node loss). The job must be idempotent or checkpointed.

## Gotchas
- `--properties` here are Spark job properties; cluster-level defaults belong to `--properties=spark:...` at cluster creation.
- Submitting needs `roles/dataproc.editor` (or a custom role with `dataproc.jobs.create`), but the job runs as the **cluster VM SA**: data access is that SA's, not the submitter's. Anyone who can submit jobs can act with the cluster SA's permissions, so scope it tightly.
- Jobs submitted with `spark-submit` over SSH bypass the Jobs API: no tracking, no restart.

## Verify
- [ ] `jobs describe` reports `DONE`; output data exists; the job shows in the Dataproc Jobs page with labels.

## Checked

2026-10-27. Confirmed: flags and commands against the gcloud reference pages, the product guides cited in sources, IAM roles pages, and API discovery documents for enums. Removed: the pinned connector jar version (now a placeholder).

Method: documentation only; no commands were run.
