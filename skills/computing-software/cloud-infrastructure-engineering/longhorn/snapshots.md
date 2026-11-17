---
id: computing-software.cloud-infrastructure-engineering.longhorn.snapshots
name: snapshots
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [snapshots, snapshot-crd, volume-head, kubectl, delete-snapshot]
level: intro
status: docs-checked
description: "Create, list and delete Longhorn snapshots from the UI or the Snapshot CRD, and how deleting the Volume Head parent differs between V1 and V2."
sources:
  - https://longhorn.io/docs/1.13.0/snapshots-and-backups/setup-a-snapshot/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: take and manage volume snapshots.

UI: Volume, open the volume, Take Snapshot. The new snapshot appears before the Volume Head.

kubectl: Longhorn uses its own `Snapshot` CRD (`longhorn.io/v1beta2`), not `VolumeSnapshot`.

```yaml
apiVersion: longhorn.io/v1beta2
kind: Snapshot
metadata:
  name: longhorn-test-snapshot
  namespace: longhorn-system
spec:
  volume: pvc-840804d8-6f11-49fd-afae-54bc5be639de   # your Longhorn volume name
  createSnapshot: true
```

```bash
kubectl apply -f longhorn-snapshot.yaml
kubectl get snapshots.longhorn.io -l longhornvolume=<volume name> -n longhorn-system
kubectl delete snapshot.longhorn.io longhorn-test-snapshot -n longhorn-system
```

If the volume is detached a warning says the engine is not running; Longhorn retries and the snapshot completes once the volume is attached.

Deleting the snapshot that is the direct parent of the Volume Head:
- V1: the Snapshot CR remains with `READYTOUSE` false and the snapshot marked `Removed`.
- V2: the Snapshot CR is removed immediately because the parent merges into the Volume Head.

The page does not cover revert or limits; see the snapshot space management skill for counts and sizes.

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/snapshots-and-backups/setup-a-snapshot/

No claim needed changing.

Method: documentation only; no commands were run.
