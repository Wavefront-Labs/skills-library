---
id: computing-software.cloud-infrastructure-engineering.velero.in-place-restore-preparation
name: in-place-restore-preparation
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [inplace-restore-prep, scale-to-zero, preflight-checks, workload-quiesce, restore-wait]
level: advanced
status: docs-checked
description: "Prepare workloads and meet Velero pre-flight checks before an in-place restore, including the FSB rule against scaling to zero."
sources:
  - https://velero.io/docs/main/volume-data-inplace-restore/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Velero does not stop workloads for you. Before an in-place restore, remove every consumer of the target PVCs, because active pods risk corruption and PVC protection or `ReadWriteOncePod` constraints block operations.

For CSI snapshot data movement (`velero-block`, `velero-fs`):
- Deployments and StatefulSets: `kubectl scale deployment NAME -n NS --replicas=0`, then wait until pods have fully terminated.
- Jobs and CronJobs: suspend CronJobs and delete running Jobs and pods.
- DaemonSets: delete temporarily (keep PVCs and PVs), or cordon and drain nodes.
- Operator-managed workloads such as ArgoCD or Flux: pause reconciliation, then delete the pods.
- External consumers such as direct NFS or iSCSI mounts: disconnect them.

For File System Backup (PodVolumeRestore): delete the workload controllers but keep PVCs and PVs.

```bash
kubectl delete deployment NAME -n NS --cascade=foreground
```

Do not just scale to zero. FSB restores through the `restore-wait` init container of the pod that Velero recreates, and a controller scaled to zero immediately terminates that pod. Include the controllers in the restore so they are recreated.

Velero validates before touching storage: the PVC is not mounted by pods in `Pending`, `Running` or `Terminating`; the PVC is `Bound`, and to the original volume handle unless mismatch is allowed; and the PV capacity is at least the backed-up data size.

## Checked

2026-11-08. Read in full against the Velero docs (main, raw markdown of volume-data-inplace-restore): https://velero.io/docs/main/volume-data-inplace-restore/. Confirmed the workload preparation steps, the FSB scale-to-zero warning and the three pre-flight checks stated above. Nothing was removed.

Method: documentation only; no commands were run.
