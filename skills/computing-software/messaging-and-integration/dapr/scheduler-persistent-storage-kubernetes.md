---
id: computing-software.messaging-and-integration.dapr.scheduler-persistent-storage-kubernetes
name: scheduler-persistent-storage-kubernetes
category: computing-software
field: messaging-and-integration
product: dapr
tags: [scheduler, etcd, persistent-volume, storage-class, pvc, helm, jobs, reminders, kubernetes]
level: advanced
status: docs-checked
description: "Size and expand Dapr Scheduler storage on Kubernetes: 1Gi default, 16Gi start, storageSize and etcdSpaceQuota, the space exceeded error, PVC expansion."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/hosting/kubernetes/kubernetes-persisting-scheduler.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Scheduler writes jobs to an embedded Etcd database and by default uses a 1Gi PVC per replica on the cluster default storage class. It backs actor reminders, workflows and the Jobs API, so 1Gi is usually too small for production; the page suggests at least 16Gi. When full it logs `error running scheduler: etcdserver: mvcc: database space exceeded`.

Etcd keeps write-ahead logs and snapshots, so disk use is often several multiples of the visible data. Jobs API and reminders map one to one with what your apps create; workflows create many short-lived reminders with small payloads.

Fresh install with 16Gi (set both the volume size and the Etcd quota):

```bash
dapr init -k --set dapr_scheduler.cluster.storageSize=16Gi --set dapr_scheduler.etcdSpaceQuota=16Gi
```

```bash
helm upgrade --install dapr dapr/dapr \
--version=<chart version> \
--namespace dapr-system \
--create-namespace \
--set dapr_scheduler.cluster.storageSize=16Gi \
--set dapr_scheduler.etcdSpaceQuota=16Gi \
--wait
```

If Dapr was installed before and the storage provider cannot expand volumes, delete the old claims so new ones are created (PVCs survive uninstall deliberately):

```bash
kubectl delete pvc -n dapr-system dapr-scheduler-data-dir-dapr-scheduler-server-0 dapr-scheduler-data-dir-dapr-scheduler-server-1 dapr-scheduler-data-dir-dapr-scheduler-server-2
```

Expanding in place needs a StorageClass with `allowVolumeExpansion: true`. Then:

1. `kubectl delete sts -n dapr-system dapr-scheduler-server --cascade=orphan`
2. `kubectl edit pvc -n dapr-system dapr-scheduler-data-dir-dapr-scheduler-server-0 ...` raising `spec.resources.requests.storage` for each replica.
3. Reinstall Dapr with the new storage size to recreate the StatefulSet.

With no default storage class define one; the page says 64Gb is more than sufficient for most production scenarios.

## Checked

2026-11-08. 1Gi default PVC, the 16Gi recommendation, the etcd error message, storageSize and etcdSpaceQuota flags for CLI and Helm, PVC deletion note, the expansion steps and the 64Gb remark confirmed on the Persist Scheduler Jobs page. All claims unchanged. The page mixes 1Gb and 1Gi for the default size.

Method: documentation only; every cited page read in full; no commands were run.
