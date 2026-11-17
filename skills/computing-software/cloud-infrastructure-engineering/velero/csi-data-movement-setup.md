---
id: computing-software.cloud-infrastructure-engineering.velero.csi-data-movement-setup
name: csi-data-movement-setup
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [csi-data-movement-setup, node-agent-disable-host-path, csisnapshotmetadataserviceconfigs, deletionpolicy, snapshot-move-data]
level: advanced
status: docs-checked
description: "Prerequisites and install flags for CSI snapshot data movement: node agent, VolumeSnapshotClass deletionPolicy, and CBT service account."
sources:
  - https://velero.io/docs/main/csi-snapshot-data-movement/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Prerequisites: Kubernetes 1.20 or later, a CSI driver supporting snapshots at the v1 API, and MountPropagation. The block data mover also needs block storage, a CSI driver with the Changed Block Tracking API, and Linux nodes for its pods.

Install:

```bash
velero install --use-node-agent --features=EnableCSI --plugins=<object storage plugin>
```

The built-in movers do not need the pod volume host path. It is created by default for fs-backup; omit it with `--node-agent-disable-host-path`.

VolumeSnapshotClass: use `deletionPolicy: Delete` for `velero-fs` and `velero-block`. After successful data movement Velero deletes the snapshot regardless, so `Retain` does not preserve it; with `Retain`, a failed or cancelled operation before the handoff can leave the source VolumeSnapshotContent and snapshot needing manual cleanup.

If the CSI CBT service needs a dedicated service account, set it in the `node-agent-config` ConfigMap:

```json
{
  "csiSnapshotMetadataServiceConfigs": {
    "saName": "<cbt-service-account-name>"
  }
}
```

and install with `--node-agent-configmap=<ConfigMap-Name>`. Velero passes `--cbt-sa-name` to the data mover pod.

Data mover pods use the priority class from the node-agent ConfigMap; the DaemonSet takes `--node-agent-priority-class-name`.

## Checked

2026-11-03. Read against the Velero docs (main): https://velero.io/docs/main/csi-snapshot-data-movement/. Confirmed the commands, flags, field names, defaults and limits stated above against those pages. Nothing was removed.

Method: documentation only; no commands were run.
