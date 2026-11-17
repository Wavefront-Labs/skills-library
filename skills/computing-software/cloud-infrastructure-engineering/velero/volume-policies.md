---
id: computing-software.cloud-infrastructure-engineering.velero.volume-policies
name: volume-policies
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [volumepolicies, volume-policy, skip, fs-backup, snapshot]
level: advanced
status: docs-checked
description: "Control per-volume backup method with volumePolicies conditions on capacity, storageClass, volume source, PVC labels, phase and mode."
sources:
  - https://velero.io/docs/main/resource-filtering/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`volumePolicies` in a resource policies ConfigMap choose how matching volumes are backed up. Backup only. Each rule has `conditions` and an `action.type`:
- `skip`: do not back up the volume data.
- `snapshot`: back up by snapshot.
- `fs-backup`: back up by file system backup.
- `custom`: use a compatible third-party BackupItemAction plugin.

Conditions:
- `capacity`: `"10Gi,100Gi"` (inclusive range), `",5Gi"` equals `"0,5Gi"`, `"5Gi,"` means 5Gi and larger; a bare `"5Gi"` fails validation.
- `storageClass`: a list such as `gp2`, `ebs-sc`.
- volume source: `nfs: {}`, `csi: {}`, or detail: for csi a `driver` (for example `aws.efs.csi.driver`), for nfs a `server` and `path`. Only nfs and csi are supported.
- `volumeTypes`: for example `emptyDir`, `configmap`.
- `pvcLabels`: all listed key/value pairs must be on the PVC; extra labels are fine.
- `pvcPhase`: `Pending`, `Bound`, `Lost`.
- `pvcVolumeMode`: `Filesystem` or `Block`, case-sensitive.
- `pvcAccessModes`: all configured modes must be present.

```yaml
version: v1
volumePolicies:
  - conditions:
      pvcPhase: [Pending, Lost]
    action:
      type: skip
  - conditions:
      nfs: {}
    action:
      type: fs-backup
```

For pod volumes (not PV-backed) only volume source filters apply.

## Checked

2026-11-03. Read against the Velero docs (main): https://velero.io/docs/main/resource-filtering/. Confirmed the commands, flags, field names, defaults and limits stated above against those pages. Rewrote the volume-source detail as prose matching the page's csi driver and nfs server/path filters. Nothing was removed.

Method: documentation only; no commands were run.
