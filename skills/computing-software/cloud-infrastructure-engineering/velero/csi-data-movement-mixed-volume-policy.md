---
id: computing-software.cloud-infrastructure-engineering.velero.csi-data-movement-mixed-volume-policy
name: csi-data-movement-mixed-volume-policy
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [mixed-data-movers, volume-policy, datamover-parameter, velero-block, velero-fs]
level: advanced
status: docs-checked
description: "Use volume policy snapshot parameters.dataMover to run velero-block and velero-fs in one Velero backup."
sources:
  - https://velero.io/docs/main/csi-snapshot-data-movement/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A cluster often mixes block volumes (AWS EBS) with file storage (EFS, Azure Files) or storage classes without CBT support. Within one backup you can use both built-in movers by adding `parameters.dataMover` to the `snapshot` action in a volume policy:

```yaml
version: v1
volumePolicies:
- conditions:
    storageClass:
    - fast-ebs-sc
  action:
    type: snapshot
    parameters:
      dataMover: velero-block
- conditions:
    storageClass:
    - efs-sc
  action:
    type: snapshot
    parameters:
      dataMover: velero-fs
```

Volumes matching a condition use that mover. Volumes that match nothing fall back to the `--data-mover` setting of the backup.

Create the policy ConfigMap in the Velero namespace and pass it:

```bash
kubectl create cm mover-policy --from-file policy.yaml -n velero
velero backup create NAME --snapshot-move-data --data-mover velero-fs --resource-policies-configmap mover-policy
```

You do not specify the mover again on restore; Velero reads data mover type, backup mode and uploader from the backup metadata.

Order matters when conditions overlap: Velero evaluates volume policies in the listed order and applies the first matching condition, so put specific storage classes before broader rules. Use `velero backup describe NAME --details` afterwards to confirm each volume used the intended mover.

## Checked

2026-11-03. Read against the Velero docs (main): https://velero.io/docs/main/csi-snapshot-data-movement/. Confirmed the commands, flags, field names, defaults and limits stated above against those pages. Nothing was removed.

Method: documentation only; no commands were run.
