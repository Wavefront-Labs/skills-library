---
id: computing-software.cloud-infrastructure-engineering.google-cloud.dataproc-clusters-and-serverless-spark
name: dataproc-clusters-and-serverless-spark
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, dataproc, spark, hadoop, serverless-spark, dataproc-serverless, ephemeral-clusters, workflow-templates, autoscaling-policies, initialization-actions, secondary-workers, preemptible-workers, gcs-connector, bigquery-connector, dataproc-metastore, hive-metastore, jupyter-dataproc, component-gateway, enhanced-flexibility-mode]
level: practitioner
status: gated
description: "Run Spark and Hadoop on GCP: Dataproc Serverless batches vs ephemeral clusters, autoscaling with Spot secondary workers, GCS not HDFS, Dataproc Metastore, workflow templates."
sources: ["https://cloud.google.com/dataproc-serverless/docs/overview", "https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/autoscaling", "https://cloud.google.com/dataproc/docs/concepts/workflows/overview", "https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/network", "https://cloud.google.com/dataproc-metastore/docs/overview", "https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/flex", "https://cloud.google.com/dataproc/docs/guides/create-cluster"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dataproc clusters and Serverless Spark

**Goal:** Spark jobs run on infrastructure that exists only while they run, read and write
GCS/BigQuery directly, share one metastore, and never sit idle on a large cluster someone forgot.

## 1. Serverless first
```bash
gcloud dataproc batches submit pyspark gs://<P>-jobs/etl/orders.py --region=europe-west1 \
  --batch=orders-etl-$(date +%s) --version=2.2 \
  --service-account=spark-etl@<P>.iam.gserviceaccount.com --subnet=dataproc \
  --properties=spark.executor.cores=4,spark.executor.memory=16g,spark.dynamicAllocation.maxExecutors=50,spark.dataproc.scaling.version=2 \
  --jars=gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-latest.jar \
  --metastore-service=projects/<P>/locations/europe-west1/services/hive-prod \
  --history-server-cluster=projects/<P>/regions/europe-west1/clusters/phs \
  --ttl=4h --labels=team=data,job=orders-etl -- --date=2026-10-15
```
- No cluster to manage: bills per DCU-hour and shuffle storage while the batch runs; autoscales executors. **Interactive sessions** (Jupyter in BigQuery Studio or Vertex Workbench) for notebooks.
- Needs a subnet with **Private Google Access** (no external IPs by design) and firewall allowing **all ingress within the subnet** (executors talk to each other). Shared VPC: Dataproc service agent needs `compute.networkUser` on the subnet.
- Persistent History Server (PHS): a tiny single-node cluster with `--enable-component-gateway` and `spark:spark.history.fs.logDirectory=gs://<P>-phs/*/spark-job-history` so Spark UIs survive after batches end.
- Custom container images (`--container-image`) for Python deps; otherwise `--py-files`/`--properties=spark.pyspark.python`.

## 2. When you still need a cluster
Legacy Hadoop/Hive/HBase, Presto/Trino, long-lived notebooks, or specific init actions. Make it **ephemeral**: create → job → delete, or set idle deletion.
```bash
gcloud dataproc clusters create etl-$(date +%s) --region=europe-west1 --image-version=2.2-debian12 \
  --master-machine-type=n2-standard-4 --num-workers=2 --worker-machine-type=n2-standard-8 \
  --num-secondary-workers=0 --secondary-worker-type=spot \
  --autoscaling-policy=etl-policy --enable-component-gateway --optional-components=JUPYTER \
  --no-address --subnet=dataproc --service-account=spark-etl@<P>.iam.gserviceaccount.com \
  --max-idle=30m --max-age=12h --dataproc-metastore=projects/<P>/locations/europe-west1/services/hive-prod \
  --initialization-actions=gs://<P>-init/install-libs.sh --metadata=... \
  --properties=dataproc:efm.spark.shuffle=primary-worker,spark:spark.sql.adaptive.enabled=true
```
- **Autoscaling policy** (YAML: `workerConfig` min/max, `secondaryWorkerConfig` min/max, `basicAlgorithm.yarnConfig` with `scaleUpFactor`, `gracefulDecommissionTimeout: 1h`) scales on YARN pending/available memory. Scale **secondary (Spot/preemptible) workers** wide and primary workers narrow; secondary workers hold no HDFS.
- **Enhanced Flexibility Mode** (`dataproc:efm.spark.shuffle=primary-worker`) keeps shuffle data off Spot workers so preemption does not re-run stages.
- Data in **GCS** (`gs://` via the GCS connector, already installed) — HDFS only as scratch; `--num-workers=2` minimum is for HDFS replication you are not using.
- Init actions run on every node at creation; keep them idempotent and fast, or build a **custom image** (`generate_custom_image.py`) for heavy deps.
- **Workflow templates** (`gcloud dataproc workflow-templates create` + `set-managed-cluster` + `add-job`) create-run-delete a cluster per DAG; instantiate from Cloud Scheduler/Composer.

## 3. Metastore and catalog
- **Dataproc Metastore** (managed Hive Metastore, gRPC/Thrift) shared by clusters, Serverless, and BigQuery (via BigLake/Metastore federation); back it up (`gcloud metastore services backups create`) and size by tier. Alternative: BigQuery metastore (newer, no server) for Iceberg tables.
- BigQuery connector (`spark-bigquery`) reads via Storage Read API (fast, billed) and writes via direct/indirect mode (indirect stages in GCS → load job, free of streaming cost).

## 4. Security and cost
- Cluster/batch SA with only the data roles + `roles/dataproc.worker`; submitters need `roles/dataproc.editor` + `iam.serviceAccountUser`. Component Gateway for UIs through IAM (no SSH tunnels); Kerberos/Ranger components for multi-tenant long-lived clusters only.
- CMEK: `--gce-pd-kms-key`; Dataproc Serverless `--kms-key`.
- Cost levers: Serverless (no idle), `--max-idle`, Spot secondary workers (60-90 % off), `n2d`/`t2d` machine types, autoscaling `scaleDownFactor` 1.0 with graceful decommission, cluster labels for billing export.
- Monitor: `dataproc.googleapis.com/cluster/yarn/pending_memory_size` (gated: unconfirmed, source is paywalled or blocked) (autoscaler signal), `batch/spark/executors`, job duration trends per label.

## Gotchas
- Serverless batch stuck in `PENDING` = subnet lacks PGA or the internal-ingress firewall rule; the error only appears after minutes.
- Autoscaling without graceful decommission kills executors mid-stage; with EFM off on Spot workers, every preemption re-computes shuffle.
- Image version pins Spark/Python versions; `2.2` vs `2.1` can break UDF pickling — pin per job, test upgrades.
- Dataproc clusters with `--no-address` need Cloud NAT only for pip/apt in init actions; Google APIs go via PGA.
- A forgotten long-lived cluster is the single most common Dataproc bill shock; alert on clusters older than `max-age` without the `persistent=true` label.

## Verify
- [ ] Serverless batch completes with executors scaling up then down (`batches describe` → `runtimeInfo.approximateUsage` (gated: unconfirmed, source is paywalled or blocked)), no external IPs anywhere.
- [ ] Cluster with `--max-idle=30m` self-deletes; workflow template run leaves no cluster behind.
- [ ] Tables created in a batch are visible from a different cluster through the shared Metastore.
- [ ] Spark UI for a finished batch opens via the PHS Component Gateway link.

## Checked

2026-10-27. Confirmed: flags and commands against the gcloud reference pages, the product guides cited in sources, IAM roles pages, and API discovery documents for enums. Removed: the nonexistent gcloud dataproc sessions group and the 20-node figure. Gated: the autoscaler pending-memory metric name and the batch runtimeInfo.approximateUsage field were not found in the fetched pages.

Method: documentation only; no commands were run.
