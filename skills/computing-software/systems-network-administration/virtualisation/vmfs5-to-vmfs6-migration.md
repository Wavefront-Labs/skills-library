---
id: computing-software.systems-network-administration.virtualisation.vmfs5-to-vmfs6-migration
name: vmfs5-to-vmfs6-migration
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vmfs6, vmfs5, vmfs, storage-vmotion, datastore-migration, vmware, vsphere]
level: practitioner
status: draft
description: "Move from VMFS5 to VMFS6 datastores with Storage vMotion (no in-place upgrade exists), including SDRS clusters, RDM pointers, and decommissioning the old LUNs."
sources:
  - https://knowledge.broadcom.com/external/article?legacyId=2147824
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VMFS5 to VMFS6 migration

**Goal:** all datastores on VMFS6 (automatic UNMAP, 4Kn support, better small-file handling) with no VM downtime.

## Why it matters
- vSphere 8 still mounts VMFS5 but cannot create it; some features (automatic space reclamation, 4Kn devices, larger number of paths) need VMFS6.
- There is **no in-place upgrade**. You create a new VMFS6 datastore and evacuate.

## Procedure (per datastore)
1. Inventory: `esxcli storage filesystem list` (Type column VMFS-5 / VMFS-6) or `Get-Datastore | Select Name, FileSystemVersion`.
2. Present a new LUN (or a free one) and create a VMFS6 datastore with the same size or larger.
3. Storage vMotion all VMs off the VMFS5 datastore:
```powershell
Get-VM -Datastore old-ds01 | Move-VM -Datastore new-ds01 -RunAsync
```
4. Move templates (convert to VM or use Move-Template), ISOs, content library items and any orphaned files (browse the datastore).
5. Check RDM pointer files: moving the VM moves the mapping file; the RDM LUN itself is not on VMFS.
6. Unmount and detach the old LUN on all hosts, then unpresent on the array.

## Datastore clusters
With SDRS, put the VMFS5 datastore into SDRS *maintenance mode*; SDRS evacuates it to the VMFS6 members automatically (VMs with affinity rules may need manual moves).

## Swing-LUN approach
Short on capacity: evacuate one VMFS5 datastore, delete it, recreate the same LUN as VMFS6, and use it as the target for the next one.

## Gotchas
- Mixed VMFS5/VMFS6 datastore clusters are allowed but SDRS prefers not to mix; finish quickly.
- vSphere Replication/SRM placeholders and backup proxies with hot-add need datastore remaps after moves.
- Snapshots: Storage vMotion consolidates nothing; large snapshot chains make the move slow. Consolidate first.

## Verify
`Get-Datastore | Group FileSystemVersion` shows only 6.x; old LUNs detached with no APD/PDL events.
