---
id: computing-software.cloud-infrastructure-engineering.rook.host-storage-cluster-device-selection
name: host-storage-cluster-device-selection
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [host-cluster, usealldevices, devicefilter, nodes, placement, node-affinity]
level: practitioner
status: docs-checked
description: "Configure a host storage cluster where mons use a host path and OSDs consume raw devices, using all devices, filters or per-node device lists."
sources:
  - https://rook.io/docs/rook/latest-release/CRDs/Cluster/host-cluster/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In a host storage cluster, Ceph mons store metadata on the host under `dataDirHostPath` and the OSDs consume raw devices or partitions.

Simplest form: consume everything.
```
spec:
  cephVersion:
    image: quay.io/ceph/ceph:v20.2.4
  dataDirHostPath: /var/lib/rook
  mon:
    count: 3
    allowMultiplePerNode: false
  storage:
    useAllNodes: true
    useAllDevices: true
```

Node and device filters: keep `useAllNodes: true` but add `deviceFilter: sdb`, a regular expression so OSDs are created only on matching devices. Use the `placement` section to control scheduling. The docs example uses `placement.all` node affinity for nodes labelled `role=rook-node`, and `placement.osd` node affinity so OSDs run only on nodes labelled `role=rook-osd-node`.

Specific nodes and devices: set both `useAllNodes` and `useAllDevices` to false and list `nodes`. Rules from the page:
- Each node `name` must match its `kubernetes.io/hostname` label.
- `devices` entries may be a short name such as `sdc1` (a partition must have no filesystem) or an explicit udev path such as `/dev/disk/by-id/...`.
- A node-level `config` overrides the cluster-level config.
- `databaseSizeMB: "1024"` can be removed on normal-sized disks of 100 GB or larger.

## Checked

2026-11-03. Read the Rook docs page(s) cited in sources (host-cluster) against this skill: 24 backticked identifiers, flags, versions and quoted strings were matched to the page text; the 0 reported as not literally matched are YAML nesting or placeholder formatting, and each was confirmed by reading the surrounding page text (nested field lists, example output, command blocks). Nothing needed removing.

Method: documentation only; no commands were run.
