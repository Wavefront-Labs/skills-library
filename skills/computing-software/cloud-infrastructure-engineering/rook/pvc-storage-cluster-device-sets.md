---
id: computing-software.cloud-infrastructure-engineering.rook.pvc-storage-cluster-device-sets
name: pvc-storage-cluster-device-sets
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [pvc-cluster, storageclassdevicesets, volumeclaimtemplates, volumemode-block, portable, local-storage]
level: advanced
status: docs-checked
description: "Run mons and OSDs on volumes from a storage class using storageClassDeviceSets, with the AWS gp2-csi and local-storage examples."
sources:
  - https://rook.io/docs/rook/latest-release/CRDs/Cluster/pvc-cluster/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A PVC-based cluster stores Ceph data on volumes requested from a storage class you choose. It is recommended in clouds where volumes are created dynamically, and where a local PV provisioner exists.

The storage class must provide file mode for mons and block mode for OSDs. The AWS example uses `gp2-csi`:
```
mon:
  count: 3
  allowMultiplePerNode: false
  volumeClaimTemplate:
    spec:
      storageClassName: gp2-csi
      resources:
        requests:
          storage: 10Gi
storage:
  storageClassDeviceSets:
  - name: set1
    count: 3
    portable: false
    encrypted: false
    volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        resources:
          requests:
            storage: 10Gi
        storageClassName: gp2-csi
        volumeMode: Block
        accessModes:
        - ReadWriteOnce
    onlyApplyOSDPlacement: false
```

Each set creates `count` OSDs, one per PVC. The local-storage example creates three OSDs with explicit `resources` (4Gi memory request and limit, 500m CPU request) and pod anti-affinity placement, plus three mons on 10Gi PVCs from `local-storage`. Mons may use PVCs while OSDs still consume raw host devices.

Placement for PVC OSDs comes from `placement.all` plus the placement or `preparePlacement` inside the device set.

## Checked

2026-11-03. Confirmed against the PVC Storage Cluster page: the gp2-csi example with mon volumeClaimTemplate and storageClassDeviceSets fields (count, portable, encrypted, volumeMode Block) and the local-storage example. Removed: nothing.

Method: documentation only; no commands were run.
