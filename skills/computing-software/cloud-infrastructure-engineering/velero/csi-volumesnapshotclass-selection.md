---
id: computing-software.cloud-infrastructure-engineering.velero.csi-volumesnapshotclass-selection
name: csi-volumesnapshotclass-selection
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [volumesnapshotclass, csi-volumesnapshot-class, snapshotclass, is-default-class, pvc-annotation]
level: advanced
status: docs-checked
description: "Control which VolumeSnapshotClass Velero uses via label, annotation, backup annotation, volume policy snapshotClass or PVC annotation."
sources:
  - https://velero.io/docs/main/csi/
  - https://velero.io/docs/main/resource-filtering/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For each CSI driver Velero picks a VolumeSnapshotClass in this way. In the order the Velero CSI page lists them (the page states that a volume policy `snapshotClass` overrides backup annotations and class labels, and that a PVC annotation overrides every other method):

1. Default by annotation: `snapshot.storage.kubernetes.io/is-default-class: "true"` on the class. A default can be set for each CSI driver.
2. Default by label: `velero.io/csi-volumesnapshot-class: "true"`. Only one class per driver may carry the label.
3. Per backup or schedule, an annotation in lowercase with the format `velero.io/csi-volumesnapshot-class_<driver name>: "<class name>"`:

```yaml
kind: Backup
metadata:
  name: test-backup
  annotations:
    velero.io/csi-volumesnapshot-class_disk.csi.cloud.com: "test-snapclass"
```

4. Volume policy: set `parameters.snapshotClass` on the `snapshot` action, useful when several storage arrays share a driver but need different classes.

```yaml
volumePolicies:
- conditions:
    storageClass:
    - nutanix-files
  action:
    type: snapshot
    parameters:
      snapshotClass: nutanix-files-snapclass
```

This overrides backup annotations and class labels.
5. PVC annotation `velero.io/csi-volumesnapshot-class: "test-snapclass"` on the PVC. This overrides every other method.

Retention: the VolumeSnapshotContent takes the DeletionPolicy of the class. `Retain` keeps the snapshot for the lifetime of the backup; when the backup expires Velero patches the content to `Delete` so space is freed.

## Checked

2026-11-03. Read against the Velero docs (main): https://velero.io/docs/main/csi/, https://velero.io/docs/main/resource-filtering/. Confirmed the commands, flags, field names, defaults and limits stated above against those pages. Reworded the default-selection ordering and the per-driver default wording to match the CSI page. Nothing was removed.

Method: documentation only; no commands were run.
