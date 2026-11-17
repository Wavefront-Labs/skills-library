---
id: computing-software.cloud-infrastructure-engineering.longhorn.storage-tags
name: storage-tags
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [storage-tags, node-tags, disk-tags, disk-selector, node-selector]
level: practitioner
status: docs-checked
description: "Restrict Longhorn replicas to tagged nodes and disks with node and disk tags and StorageClass diskSelector and nodeSelector."
sources:
  - https://longhorn.io/docs/1.13.0/nodes-and-volumes/nodes/storage-tags/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pin replicas to a class of storage such as `fast`, `ssd` or `nvme` disks, or `baremetal` nodes.

Tag nodes and disks: UI, Node, select node, Edit Node and Disks, then `+New Node Tag` or `+New Disk Tag`. New tags do not affect replicas already scheduled.

Matching: when a volume requests several tags, both the disk and its parent node must carry all requested tags.

Request tags:
- UI: set the disk tag and node tag when creating the volume.
- StorageClass parameters: `diskSelector` (for example `"ssd"`) and `nodeSelector` (comma-separated, for example `"storage,fast"`).

```yaml
parameters:
  numberOfReplicas: "3"
  diskSelector: "ssd"
  nodeSelector: "storage,fast"
```

Defaults:
- Default StorageClass: add the parameters to the `longhorn-storageclass` ConfigMap.
- Helm: set `persistence.defaultNodeSelector` in `values.yaml`.
- Custom StorageClass: put `diskSelector` and `nodeSelector` in its `parameters`.

Available since v0.6.0.

## Checked

2026-11-08. Confirmed against: https://longhorn.io/docs/1.13.0/nodes-and-volumes/nodes/storage-tags/. Purpose and example tags, UI setup path, no effect on already-scheduled replicas, all-tags matching rule, UI and StorageClass usage, the longhorn-storageclass ConfigMap, Helm persistence.defaultNodeSelector, custom StorageClass, v0.6.0.

Removed or reworded: The Allow Empty Node/Disk Selector Volume settings and their defaults (not on the cited page).

Method: documentation only; no commands were run.
