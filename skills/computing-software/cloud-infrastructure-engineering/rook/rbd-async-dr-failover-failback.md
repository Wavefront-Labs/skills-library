---
id: computing-software.cloud-infrastructure-engineering.rook.rbd-async-dr-failover-failback
name: rbd-async-dr-failover-failback
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [failover, failback, volumereplication, replicationstate, planned-migration, disaster-recovery]
level: sme
status: docs-checked
description: "Planned migration between mirrored RBD clusters by demoting the primary with VolumeReplication and recreating PVC and PV on the secondary."
sources:
  - https://rook.io/docs/rook/latest-release/Storage-Configuration/Block-Storage-RBD/rbd-async-disaster-recovery-failover-failback/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rook's volume replication support allows disaster recovery and planned migration (datacenter maintenance, technology refresh, disaster avoidance). It assumes RBD mirroring is set up between the peers.

Relocation switches production to the backup site. Access on the primary must stop, then the image is made primary on the secondary cluster.

Planned migration, primary (cluster-1) to secondary (cluster-2):
1. Scale down all application pods using the mirrored PVC on the primary.
2. Back up the PVC and PV objects from the primary, for example with Velero.
3. Set the VolumeReplication CR `replicationState` to `secondary` on the primary site. The operator passes this to the driver by gRPC to mark the data source secondary.
4. If recreating PVC and PV manually on the secondary, remove the `claimRef` section from the PV objects.
5. Recreate the StorageClass, PVC and PV on the secondary. Static binding means the PVC binds to the existing PV and no new PV is created.
6. Create the VolumeReplicationClass on the secondary.
7. Create VolumeReplications for each mirrored PVC with `replicationState: primary`, then check the CR status shows the image primary.
8. Scale the applications up.

In a disaster-recovery failover you only get crash-consistent data up to the last snapshot interval, not complete data. Failback follows the same primary and secondary swap after the failed site returns.

## Checked

2026-11-03. Confirmed against the RBD Async DR failover and failback page: the planned migration steps, replicationState secondary and primary, removing claimRef, static binding, and crash-consistent data only up to the snapshot interval. Removed: nothing.

Method: documentation only; no commands were run.
