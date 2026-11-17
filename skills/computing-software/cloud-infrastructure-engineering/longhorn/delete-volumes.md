---
id: computing-software.cloud-infrastructure-engineering.longhorn.delete-volumes
name: delete-volumes
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [delete-volumes, reclaim-policy, pvc, ui, attached-volume]
level: intro
status: docs-checked
description: "Delete Longhorn volumes through Kubernetes PVC deletion with a Delete reclaim policy or through the UI, and the effect on PVs and PVCs."
sources:
  - https://longhorn.io/docs/1.13.0/nodes-and-volumes/volumes/delete-volumes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: remove a volume and its data.

Via Kubernetes: works only if the volume was provisioned by a StorageClass and its PV has reclaim policy `Delete`. Delete the PersistentVolumeClaim; Kubernetes cleans up the PV, then deletes the volume in Longhorn.

```bash
kubectl delete pvc <pvc-name> -n <namespace>
```

Via the Longhorn UI (any volume, however created):
- Single: Volumes page, Operation dropdown, Delete, confirm.
- Multiple: tick the volumes, then Delete at the top.

Side effects:
- If the volume is tied to a PV or PVC, Longhorn deletes those too; the UI warns first.
- Longhorn warns when you delete an attached volume because it may be in use.

Check the reclaim policy first. Because the Kubernetes route works only with reclaim policy `Delete`, a volume whose PV uses another policy has to be deleted in the UI.

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/nodes-and-volumes/volumes/delete-volumes/

Removed: the claim that backups on the backup target survive volume deletion (not on the page). The Retain remark is now stated only as the implication of the page note that the Kubernetes route needs reclaim policy Delete.

Method: documentation only; no commands were run.
