---
id: computing-software.cloud-infrastructure-engineering.velero.data-movement-restore-pvc-and-cache
name: data-movement-restore-pvc-and-cache
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [restorepvc, ignoredelaybinding, cachepvc, thresholdingb, waitforfirstconsumer]
level: sme
status: docs-checked
description: "Tune DataDownload with restorePVC ignoreDelayBinding and a cachePVC for large restores in the node-agent ConfigMap."
sources:
  - https://velero.io/docs/main/supported-configmaps/node-agent-configmap/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two node-agent ConfigMap sections tune CSI snapshot data movement restore (DataDownload pods).

`restorePVC` configures the intermediate PVC:

```json
{
  "restorePVC": {
    "ignoreDelayBinding": true
  }
}
```

- `ignoreDelayBinding`: ignore `WaitForFirstConsumer` binding constraints so the volume is provisioned without a pod being scheduled. This improves restore parallelism, but the volume may land on a node where the workload pod cannot run. Use only when you understand your topology, ideally with node selection.
- `secretNames` and `configMapNames`: copied from the target restore namespace to the Velero namespace before the restore PVC is created, then deleted after the DataDownload completes (for example `ceph-csi-kms-token`).

`cachePVC` caches downloaded data locally:

```json
{
  "cachePVC": {
    "thresholdInGB": 1,
    "storageClass": "cache-optimized-storage"
  }
}
```

- `thresholdInGB`: minimum backup data size in GB that triggers creating a cache PVC.
- `storageClass`: class for the cache PVCs.

The cache PVC exists only when restored data exceeds the threshold, must be on a class with enough capacity, and is cleaned up after the restore. It reduces repeated downloads from object storage on large volumes.

## Checked

2026-11-03. Read against the Velero docs (main): https://velero.io/docs/main/supported-configmaps/node-agent-configmap/. Confirmed the commands, flags, field names, defaults and limits stated above against those pages. Nothing was removed.

Method: documentation only; no commands were run.
