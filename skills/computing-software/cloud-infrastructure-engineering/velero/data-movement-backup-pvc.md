---
id: computing-software.cloud-infrastructure-engineering.velero.data-movement-backup-pvc
name: data-movement-backup-pvc
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [backuppvc, readonly, spcnorelabeling, readwriteoncepod, backup-pvc-secretnames]
level: sme
status: docs-checked
description: "Configure the intermediate BackupPVC for DataUpload: storage class mapping, readOnly, SELinux spcNoRelabeling and copied secrets."
sources:
  - https://velero.io/docs/main/supported-configmaps/node-agent-configmap/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`backupPVC` in the node-agent ConfigMap configures the intermediate PVC that DataUpload pods mount. It is keyed by the source storage class name:

```json
{
  "backupPVC": {
    "source-storage-class": {
      "storageClass": "backup-optimized-class",
      "readOnly": true,
      "spcNoRelabeling": true
    }
  }
}
```

Options:
- `storageClass`: alternative class for the backup PVC; defaults to the source PVC class.
- `readOnly`: `true` sets access mode `ReadOnlyMany` only, otherwise `ReadWriteOnce`. Avoids a full data clone on some providers, such as Ceph RBD.
- `spcNoRelabeling`: `true` sets the pod SELinux type to `spc_t`, disabling enforcement and volume relabeling.
- `readWriteOncePod`: `true` sets `ReadWriteOncePod` only so the kubelet labels the volume at mount time instead of relabeling each file; needs a CSI driver with `seLinuxMount: true`. Ignored if `readOnly` is true.
- `secretNames` and `configMapNames`: objects copied from the source PVC namespace to the Velero namespace before creating the PVC, and deleted after the DataUpload completes. Needed by drivers that require namespaced secrets, for example `ceph-csi-kms-token`.

Notes: the specified classes must exist and support the access modes. In SELinux environments always set `spcNoRelabeling: true` with `readOnly: true`. A failure leaves the DataUpload in `Accepted` until the 30m default timeout.

## Checked

2026-11-03. Read against the Velero docs (main): https://velero.io/docs/main/supported-configmaps/node-agent-configmap/. Confirmed the commands, flags, field names, defaults and limits stated above against those pages. Nothing was removed.

Method: documentation only; no commands were run.
