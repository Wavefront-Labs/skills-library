---
id: computing-software.cloud-infrastructure-engineering.longhorn.csi-volume-clone
name: csi-volume-clone
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [clone, csi, datasource, linked-clone, full-copy]
level: practitioner
status: docs-checked
description: "Clone a Longhorn volume with a PVC dataSource, the same-size rule, and V2 full-copy versus linked-clone modes with their constraints."
sources:
  - https://longhorn.io/docs/1.13.0/snapshots-and-backups/csi-volume-clone/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: create a PVC with the same content as an existing one.

V1:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: cloned-pvc
spec:
  storageClassName: longhorn
  dataSource:
    name: source-pvc
    kind: PersistentVolumeClaim
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

`cloned-pvc` must have the same `resources.requests.storage` as `source-pvc`. Other requirements follow upstream CSI volume cloning rules.

V2 needs a StorageClass with `dataEngine: "v2"`:
- `full-copy`: the same `dataSource` YAML with the V2 class; Longhorn copies the data to a fully independent PVC.
- `linked-clone`: shares data blocks with the source by copy-on-write and creates all replicas at creation, so no rebuild is needed. Requires a StorageClass with `cloneMode: "linked-clone"`.

Linked-clone constraints:
- supported only on V2
- replica count cannot exceed the source's
- each linked-clone replica must be on the same node and disk as a source replica
- the source's replica count cannot drop below the number backing linked clones
- the source's entrypoint snapshot cannot be deleted while linked clones exist

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/snapshots-and-backups/csi-volume-clone/

No claim needed changing.

Method: documentation only; no commands were run.
