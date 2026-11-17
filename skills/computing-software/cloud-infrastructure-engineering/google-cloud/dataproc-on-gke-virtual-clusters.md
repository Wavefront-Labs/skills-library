---
id: computing-software.cloud-infrastructure-engineering.google-cloud.dataproc-on-gke-virtual-clusters
name: dataproc-on-gke-virtual-clusters
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, dataproc, dataproc-on-gke, gke, spark-on-kubernetes, node-pools]
level: advanced
status: docs-checked
description: "Run Spark through the Dataproc API on an existing GKE cluster: virtual cluster creation, node pool roles, Workload Identity, and cleanup."
sources: ["https://docs.cloud.google.com/managed-spark/docs/guides/dpgke/quickstarts/dataproc-gke-quickstart-create-cluster", "https://docs.cloud.google.com/managed-spark/docs/guides/dpgke/gke-node-pools"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dataproc on GKE

A Dataproc (now documented as Managed Service for Apache Spark) "virtual cluster" is a virtual resource
with no master or worker VMs. Jobs run as pods on node pools of a GKE cluster you own, and the node
pools and pod scheduling are managed by GKE. Each virtual cluster has its own properties (Spark engine
version, workload identity) and is isolated in its own GKE namespace. Several virtual clusters can share node pools.

## 1. Prerequisites
- A GKE **Standard** (not Autopilot) zonal or regional cluster with **Workload Identity** enabled.
- Your user needs `roles/dataproc.editor` on the project and `roles/iam.serviceAccountUser` on the
  Compute Engine default service account; that service account needs `roles/dataproc.worker`.
- The region must match the GKE cluster's region. Creating a virtual cluster is not supported in the console.

## 2. Create the virtual cluster
```bash
gcloud dataproc clusters gke create spark-vc --region=<REGION> \
  --gke-cluster=<GKE_CLUSTER> --gke-cluster-location=<ZONE_OR_REGION> \
  --spark-engine-version=latest --staging-bucket=<BUCKET> \
  --pools='name=dp-default,roles=default,machineType=e2-standard-4' \
  --pools='name=dp-driver,roles=spark-driver,machineType=n2-standard-4,min=1,max=3' \
  --pools='name=dp-exec,roles=spark-executor,machineType=n2-standard-8,min=1,max=10' \
  --setup-workload-identity
```
- Roles: `default`, `spark-driver`, `spark-executor`. At least one pool must have `default`; the other roles
  are optional, and Google recommends separate pools per role sized for it. A pool needs a name and role;
  other settings are optional. All pools must share a location.
- `--setup-workload-identity` creates the bindings that let the Kubernetes service accounts act as the
  virtual cluster's default data-plane service account (it needs elevated permissions to set up).
- Pool settings include `machineType`, `minNodeCount`, `maxNodeCount`, `preemptible`, `spot` and accelerators.
- `--staging-bucket` is optional: if omitted, a staging bucket is created.

## 3. Submit
```bash
gcloud dataproc jobs submit spark --cluster=spark-vc --region=<REGION> \
  --class=org.apache.spark.examples.SparkPi \
  --jars=local:///usr/lib/spark/examples/jars/spark-examples.jar -- 1000
```

## Gotchas
- Deleting a virtual cluster does not delete its node pools; they are deleted with the GKE cluster, or
  delete them yourself when no cluster uses them.
- Check the current docs for job types supported on GKE virtual clusters before moving non-Spark work.

## Verify
- [ ] `gcloud dataproc clusters describe spark-vc --region=<REGION>` shows a RUNNING cluster and the SparkPi job completes.

## Checked
2026-10-28. Confirmed against the Managed Service for Apache Spark on GKE quickstart (prerequisites, roles,
`gke create` flags, namespace isolation, node pool deletion, job submit examples) and the node pool page
(roles, settings, pool deletion). Commands were checked against the gcloud reference. Removed: the
Dataproc service agent role claim, Hive/Pig/HDFS limits, `controller` role, `kubectl` namespace line and
the Serverless comparison.
Method: documentation only; no commands were run.
