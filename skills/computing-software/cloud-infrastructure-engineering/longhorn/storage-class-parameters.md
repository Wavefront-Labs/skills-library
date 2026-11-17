---
id: computing-software.cloud-infrastructure-engineering.longhorn.storage-class-parameters
name: storage-class-parameters
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [storageclass, parameters, replicas, fstype, data-engine]
level: practitioner
status: docs-checked
description: "Longhorn StorageClass fields and parameters with defaults and allowed values: replicas, fsType, dataLocality, selectors, encryption, V2 options."
sources:
  - https://longhorn.io/docs/1.13.0/references/storage-class-parameters/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: write a correct Longhorn StorageClass.

Built-in fields: `provisioner: driver.longhorn.io`, `allowVolumeExpansion` (default `true`), `reclaimPolicy` (default `Delete`), `volumeBindingMode` (`Immediate` default or `WaitForFirstConsumer`), `mountOptions`, `allowedTopologies`.

Parameters (default, values):
- `numberOfReplicas`: 3; 1 to 20 (must be 1 with `strict-local`)
- `staleReplicaTimeout`: 2880 minutes
- `fsType`: `ext4` or `xfs`; `mkfsParams` adds mkfs arguments
- `dataLocality`: `disabled`, `best-effort`, `strict-local`
- `replicaAutoBalance`: `ignored`, `disabled`, `least-effort`, `best-effort`
- `diskSelector`, `nodeSelector`: comma-separated tags
- `recurringJobSelector`: JSON array
- `encrypted`, `migratable`: `true` or `false` (default `false`)
- `fromBackup`, `backupTargetName` (`default`), `backupBlockSize` (for example `2Mi`, `16Mi`)
- `backingImage` (the sample YAML comments say `backingImageName`), `backingImageChecksum`, `backingImageMinNumberOfCopies`
- `nfsOptions`; `disableRevisionCounter` (`true` in the parameter list; the sample YAML comment shows `false`)
- `replicaSoftAntiAffinity`, `replicaZoneSoftAntiAffinity`, `replicaDiskSoftAntiAffinity`: `ignored`, `enabled`, `disabled`
- `dataEngine`: `v1` or `v2`; `frontend`: V1 `blockdev` or `iscsi`; V2 `blockdev`, `nvmf`, `ublk`
- `freezeFilesystemForSnapshot` (the sample YAML comment says `freezeFSForSnapshot`), `unmapMarkSnapChainRemoved`: `ignored`, `enabled`, `disabled`
- `strictTopology` (needs `WaitForFirstConsumer`), `volumeTopology`: `any`, `zonal`, `regional`

```yaml
kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: longhorn-example
provisioner: driver.longhorn.io
allowVolumeExpansion: true
reclaimPolicy: Delete
volumeBindingMode: Immediate
parameters:
  numberOfReplicas: "3"
  staleReplicaTimeout: "2880"
  fsType: "ext4"
```

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/references/storage-class-parameters/

Added page conflicts: parameter list says backingImage, freezeFilesystemForSnapshot and disableRevisionCounter default true, while the sample YAML comments say backingImageName, freezeFSForSnapshot and false.

Method: documentation only; no commands were run.
