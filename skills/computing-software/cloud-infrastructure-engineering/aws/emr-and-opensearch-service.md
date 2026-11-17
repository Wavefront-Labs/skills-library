---
id: computing-software.cloud-infrastructure-engineering.aws.emr-and-opensearch-service
name: emr-and-opensearch-service
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, emr, opensearch, emr-serverless, emr-on-eks, emr-on-ec2, spark, hive, presto, trino, instance-fleets, managed-scaling, emrfs, opensearch-service, opensearch-serverless, opensearch-domains, ultrawarm, cold-storage, index-state-management, fine-grained-access-control, dedicated-master-nodes, shards]
level: practitioner
status: draft
description: "Run big-data compute on Amazon EMR (EC2 fleets, Serverless or EKS; managed scaling, Spot, S3 storage) and search on Amazon OpenSearch Service (sizing, shards, UltraWarm, ISM, fine-grained access)."
sources: ["Amazon EMR Management Guide - Cluster configuration, instance fleets and managed scaling", "Amazon EMR Serverless User Guide", "Amazon OpenSearch Service Developer Guide - Sizing domains and operational best practices", "Amazon OpenSearch Service Developer Guide - Index State Management and UltraWarm"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EMR and OpenSearch Service — Spark without owning Hadoop, search without owning Lucene nodes

**Goal:** batch/streaming Spark that scales to the job and shuts down after it, and an
OpenSearch domain whose shards, storage tiers and access control are sized for the data and
the people.
(Elasticsearch/OpenSearch internals — mappings, shard sizing — are covered under
`computing-software.database-administration.elasticsearch.*`; this skill covers the AWS-managed layer.)

## 1. EMR: pick the deployment
| Option | Use when |
|---|---|
| **EMR Serverless** | Spark/Hive jobs with no cluster management; pay per vCPU/memory-second; cold start seconds with pre-initialised capacity. Default for new batch work. |
| **EMR on EC2** | Long-running clusters, HBase/Flink/Presto-Trino, custom AMIs, fine control of instance types, Spot fleets. |
| **EMR on EKS** | Already running EKS; share capacity; Spark jobs as Kubernetes workloads via virtual clusters. |
| **EMR Studio / Notebooks** | Interactive dev against any of the above. |

## 2. EMR on EC2 the right way
- Release label pinned (`emr-7.x`), applications only what you use (Spark, Hadoop, Livy).
- **Instance fleets** (not groups): master on-demand; core on-demand or mixed (HDFS lives
  here — Spot cores lose HDFS blocks); **task** nodes on Spot across several types with
  `price-capacity-optimized`. Use **S3 as the data store** (EMRFS, `s3://`) so clusters are
  disposable; HDFS only as scratch.
- **Managed scaling** (`--managed-scaling-policy` min/max units, on-demand limit) scales
  task/core capacity on YARN metrics; disable autoscaling rules in favour of it.
- Transient clusters: `aws emr create-cluster … --steps file://steps.json --auto-terminate`
  per pipeline run (Step Functions `emr:createCluster.sync` → `addStep.sync` → `terminateCluster`);
  or `--auto-termination-policy IdleTimeout=3600` for interactive clusters.
- Config classifications: `spark-defaults` (`spark.sql.adaptive.enabled=true`, dynamic
  allocation), `hive-site` for Glue Data Catalog (`hive.metastore.client.factory.class=com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory`),
  `emrfs-site` for retries. Security configuration: encryption at rest/in transit, Kerberos or
  **IAM roles for EMRFS** / Lake Formation integration, Runtime roles for jobs.
- Bootstrap actions install libs on every node; keep them idempotent and in S3.
- Monitor: `YARNMemoryAvailablePercentage`, `ContainerPendingRatio`, `IsIdle`, `MRLostNodes`; logs to S3 (`--log-uri`) with
  Spark history server via persistent app UIs.

## 3. EMR Serverless
```bash
aws emr-serverless create-application --type SPARK --release-label emr-7.2.0 --name etl \
  --initial-capacity '{"DRIVER":{"workerCount":1,"workerConfiguration":{"cpu":"2vCPU","memory":"8GB"}},"EXECUTOR":{"workerCount":4,"workerConfiguration":{"cpu":"4vCPU","memory":"16GB"}}}' \
  --maximum-capacity '{"cpu":"400vCPU","memory":"1600GB"}' --auto-stop-configuration enabled=true,idleTimeoutMinutes=15
aws emr-serverless start-job-run --application-id <id> --execution-role-arn <role> \
  --job-driver '{"sparkSubmit":{"entryPoint":"s3://jobs/etl.py","sparkSubmitParameters":"--conf spark.executor.memory=16g"}}' \
  --configuration-overrides '{"monitoringConfiguration":{"s3MonitoringConfiguration":{"logUri":"s3://logs/emr-s/"}}}'
```
- Pre-initialised capacity trades idle cost for start latency; `maximum-capacity` is the cost cap.
- Architecture `ARM64` (Graviton) cheaper; custom images from ECR for Python deps; VPC
  access via subnets/SGs if the job reads RDS/MSK.

## 4. OpenSearch Service domains
- **Sizing**: storage = source bytes × (1 + replicas) × 1.1 (indexing overhead) × 1.15
  (OS reserve) → choose data node count/type (`r6g`/`or1` with S3-backed indexes for
  log analytics); **shards**: aim 10–30 GB per shard for search, up to 50 GB for logs;
  keep total shards per node ≤ ~25 × JVM heap GiB (rule of thumb).
- **3 dedicated master nodes** (never 2, never 4) for any production domain; **3 AZs** with
  `zone awareness`; replicas ≥ 1. Multi-AZ with standby for 99.99 %.
- **Storage tiers**: hot (EBS gp3/instance store) → **UltraWarm** (S3-backed, read-only,
  cheap for older logs) → **cold** (detached, pay S3 only). Move with **Index State
  Management** (ISM) policies: `rollover` at 50 GB/1 d → `warm_migration` after 7 d →
  `cold_migration` after 30 d → `delete` after 365 d.
- **Fine-grained access control** (FGAC) with the internal user DB or SAML/Cognito for
  Dashboards; roles map index patterns + field/document-level security; domain access policy
  restricts to VPC/roles. Always VPC-only domains for internal data; public endpoint only behind a strict resource policy.
- Ingest: Firehose (logs), **OpenSearch Ingestion** (managed Data Prepper pipelines for
  logs/traces/S3), Logstash/Fluent Bit, `_bulk` from apps (5–15 MB batches, retry 429s with backoff).
- **OpenSearch Serverless** collections (search / time-series / vector) when you do not want
  to size nodes; OCU-based billing with a minimum, limits on some features — check before choosing.
- Operations: blue/green deployments on config changes (expect double capacity briefly);
  snapshots automatic hourly (14 d) + manual to your S3 for cross-domain restore;
  alarms: `ClusterStatus.red/yellow`, `FreeStorageSpace` < 25 %, `JVMMemoryPressure` > 80 %,
  `ThreadpoolWriteQueue`/`Rejected`, `CPUUtilization`, `MasterReachableFromNode`.

## Gotchas
- EMR core nodes on Spot + HDFS replication 1 = lost blocks = failed job; keep HDFS off Spot or replicate to 2–3.
- EMR Serverless jobs reading from a VPC-only resource without subnets configured fail with timeouts.
- OpenSearch red status after a node loss with `replicas: 0`: data is gone; replicas are not optional.
- Too many small shards (thousands) exhaust master heap; `_cat/shards` count vs heap rule.
- FGAC + domain access policy both apply; a Kibana 403 is usually a missing role mapping, not the policy.
- Changing instance type/AZ count triggers blue/green; do it off-peak and with `FreeStorageSpace` headroom.
- Unconfirmed: current OpenSearch Service instance families (`or1`) availability and Serverless minimum OCUs — check pricing/docs.

## Verify
- [ ] EMR job run (Serverless or transient cluster) completes and the application/cluster shows `STOPPED`/`TERMINATED` after idle timeout.
- [ ] Spot task-node interruption during a Spark job does not fail it (stages retry on other executors).
- [ ] OpenSearch domain: 3 masters, 3 AZs, replicas ≥ 1, status green; `_cat/shards` within the heap rule.
- [ ] ISM policy moved yesterday's index to warm (check `_cat/indices` and the policy explain API).
- [ ] An FGAC-restricted user sees only their index pattern and masked fields in Dashboards.
