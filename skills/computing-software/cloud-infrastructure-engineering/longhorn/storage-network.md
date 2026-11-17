---
id: computing-software.cloud-infrastructure-engineering.longhorn.storage-network
name: storage-network
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [storage-network, multus, network-attachment-definition, instance-manager, rwx]
level: advanced
status: docs-checked
description: "Move Longhorn replication traffic to a Multus network with the storage-network setting, NAD format, detach-first rules and RWX caveats."
sources:
  - https://longhorn.io/docs/1.13.0/advanced-resources/deploy/storage-network/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: put Longhorn data traffic on a dedicated network.

Requirements: Multus installed. The Storage Network setting takes a Multus NetworkAttachmentDefinition (NAD), and the NAD must be reachable between pods on different nodes. Test with a simple DaemonSet and ping between its pods.

Value format: `<NAMESPACE>/<NAME>` of the NAD.

Set it:
- at install: the `storage-network` default setting
- after install: the Storage Network setting in Longhorn

Effects: Longhorn adds the `k8s.v1.cni.cncf.io/networks` annotation and recreates the instance-manager and backing-image-manager pods.

Rules:
- Do not edit a NAD after applying it; create a new NAD and point the setting at it.
- An invalid NAD stops instance-manager starting. Inspect with:

```bash
kubectl -n longhorn-system describe pods -l longhorn.io/component=instance-manager
```

- Stop workloads and detach all Longhorn volumes before changing the setting. If volumes stay attached, it applies to the instance manager only when no engines or replicas run; reconfigure after detaching or wait about an hour for the next sync.
- For RWX volumes on the endpoint network, NFS mounts must be re-established if the CSI plugin pod restarts; the setting Automatically Delete Workload Pod when The Volume Is Detached Unexpectedly helps.

The page gives no NAD manifest; see the Multus documentation for NAD configuration.

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/advanced-resources/deploy/storage-network/

No claim needed changing.

Method: documentation only; no commands were run.
