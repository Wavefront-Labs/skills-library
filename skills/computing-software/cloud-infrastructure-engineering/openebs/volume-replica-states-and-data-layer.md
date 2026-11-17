---
id: computing-software.cloud-infrastructure-engineering.openebs.volume-replica-states-and-data-layer
name: volume-replica-states-and-data-layer
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [replica, volume, data-layer, rebuild, architecture, storage-layer, nexus]
level: practitioner
status: docs-checked
description: "Know what a volume replica is on each storage layer and the five replica states (Initializing, Healthy, Offline, Rebuilding, Terminating) the OpenEBS architecture page defines."
sources:
  - https://openebs.io/docs/concepts/architecture
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In OpenEBS the volume data layer places a **volume replica** on top of the storage layer, and a replica is pinned to a node. What it is made of depends on the storage underneath:

- a sub-directory, when the storage layer is a filesystem directory;
- a full or partitioned device, when the storage layer is block devices;
- a logical volume, when the storage layer is a device pool coming from Local Storage.

If an application only needs local storage, the persistent volume is created from one of those three and the control plane provisions it. When high availability is needed, Replicated Storage adds a light-weight controller that receives read and write operations over a network endpoint and passes them to the underlying storage, and OpenEBS keeps a synchronous copy of the volume across nodes through those replica endpoints.

A replica moves through these documented states:

1. **Initializing**: being provisioned and registered to its volume.
2. **Healthy**: able to take part in reads and writes.
3. **Offline**: the node or storage hosting it has failed.
4. **Rebuilding**: the failure has been fixed and the replica is receiving data from healthy replicas.
5. **Terminating**: the volume was deleted and space is being reclaimed.

The storage layer itself (PCIe, SAS or NVMe disks, remote SAN or cloud volumes, or a directory on a mounted filesystem) is outside the data engines and reaches Kubernetes through ordinary operating system constructs.

## Checked

Method: 2026-11-08 read the raw markdown of the cited architecture page in full; the replica layer descriptions and the five states match the page and are unchanged.
