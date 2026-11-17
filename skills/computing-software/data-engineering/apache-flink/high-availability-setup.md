---
id: computing-software.data-engineering.apache-flink.high-availability-setup
name: high-availability-setup
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, flink-deployment, flink-high-availability, kubernetes-ha, zookeeper-ha, jobmanager-failover, flink-kubernetes-operator, leader-election]
level: practitioner
status: docs-checked
description: "Configure Flink JobManager high availability with Kubernetes or ZooKeeper services: HA storage, cluster IDs, standby JobManagers, operator settings, cleanup and failover testing."
sources:
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/deployment/ha/overview/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/deployment/ha/kubernetes_ha/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/deployment/ha/zookeeper_ha/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/deployment/resource-providers/yarn/
  - https://github.com/apache/flink-kubernetes-operator/blob/main/docs/content/docs/managing/job-management.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flink high availability

**Goal:** a JobManager crash or pod eviction resumes running jobs from the latest checkpoint automatically, instead of losing them.

## 1. What HA does
Without HA, the JobManager is a single point of failure: if it dies, job metadata is gone and jobs must be resubmitted (from a savepoint, manually). With HA:
- a leader election service picks the active JobManager;
- JobManager metadata (job graphs and **pointers to the latest completed checkpoints**) is persisted in `high-availability.storageDir`, with only a pointer kept in the HA service;
- a new (or standby) JobManager recovers jobs from those checkpoints.
HA does not replace checkpointing — enable both.

## 2. Kubernetes HA (preferred on Kubernetes)
```yaml
high-availability.type: kubernetes
high-availability.storageDir: s3://<flink-ha-bucket>/recovery
kubernetes.cluster-id: orders-enricher            # unique per Flink cluster
execution.checkpointing.dir: s3://<flink-state-bucket>/checkpoints
```
- Uses ConfigMaps for leader election and holds only a pointer to the metadata (stored in `high-availability.storageDir`); the service account needs permissions to create, edit and delete ConfigMaps.
- Standby JobManagers: `kubernetes.jobmanager.replicas` greater than 1 (default 1) starts standby JobManagers for faster recovery.

With the Flink Kubernetes Operator (`FlinkDeployment`):
```yaml
spec:
  flinkConfiguration:
    high-availability.type: kubernetes
    high-availability.storageDir: s3://<flink-ha-bucket>/recovery
  jobManager: {replicas: 1, resource: {memory: "2048m", cpu: 1}}
  job: {upgradeMode: last-state}       # needs HA metadata; savepoint is the other safe option
```
`upgradeMode: last-state` (alongside `stateless` and `savepoint`) uses the HA metadata or latest checkpoint information, and does not need a healthy job; manual recovery may be needed if HA metadata is lost.

## 3. ZooKeeper HA (YARN / standalone)
```yaml
high-availability.type: zookeeper
high-availability.zookeeper.quorum: zk1:2181,zk2:2181,zk3:2181
high-availability.zookeeper.path.root: /flink
high-availability.cluster-id: /orders-enricher     # customize per cluster; do not set on YARN or native Kubernetes
high-availability.storageDir: hdfs:///flink/recovery
```
On YARN, `yarn.application-attempts` limits ApplicationMaster restarts (default 1, or 2 when HA is enabled); the cluster ID is not set manually on YARN.

## 4. Gotchas
- **Unique cluster IDs.** Two clusters sharing an ID recover each other's jobs — corrupting both. Never copy configs without changing the ID.
- HA storage must be durable shared storage (S3/GCS/HDFS), not a local volume.
- On Kubernetes, `kubectl delete deployment <cluster-id>` removes the cluster resources but retains the HA ConfigMaps (they have no owner reference), so restarting with the same cluster ID recovers the previous jobs from the latest successful checkpoint. Remove the HA data deliberately when retiring a cluster, or cancel the jobs first.
- Checkpoint retention: `execution.checkpointing.num-retained` defaults to 1; consider a higher value so one bad checkpoint is not the only restore point.

## 5. Test failover
```bash
kubectl delete pod <active-jobmanager-pod>
# job should return to RUNNING from the latest checkpoint; check restored checkpoint ID in the UI / logs
```

## Checked

2026-10-25 against the Apache Flink 2.3.0 documentation (release-2.3 branch on GitHub). Confirmed from the HA overview, Kubernetes HA, ZooKeeper HA and YARN pages, the generated configuration tables (`kubernetes.jobmanager.replicas` default 1, `yarn.application-attempts`, `execution.checkpointing.dir|num-retained`) and the Flink Kubernetes Operator job-management page (`upgradeMode`). Replaced the removed 1.x checkpoint keys and removed unconfirmed ConfigMap names, pod labels and the example attempt count.

Method: documentation only; no commands were run.

## Verify
- [ ] Killing the JobManager pod recovers the job without manual action.
- [ ] Restored checkpoint is the latest completed one (no large reprocessing gap).
- [ ] Every Flink cluster has a unique cluster ID and HA path.
