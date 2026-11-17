---
id: computing-software.systems-network-administration.virtualisation.vsphere-virtual-volumes-vvols
name: vsphere-virtual-volumes-vvols
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vvols, virtual-volumes, vasa-provider, storage-container, protocol-endpoint, spbm, vsphere-storage, vmware, vsphere]
level: advanced
status: draft
description: "Deploy vSphere Virtual Volumes: register the VASA provider, create storage containers and protocol endpoints, map array capabilities to policies, and keep VASA healthy."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-storage-8-0/working-with-virtual-volumes.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# vSphere Virtual Volumes (vVols)

**Goal:** per-VM-disk storage objects on the array, managed by storage policy, so
snapshots, replication and QoS happen per VM instead of per LUN.

## Components
| Piece | What it is |
|---|---|
| VASA provider | Array (or appliance) service registered in vCenter; exposes capabilities and creates vVols |
| Storage container | Logical pool on the array; shows as a vVol datastore |
| Protocol endpoint (PE) | The I/O access point (a small LUN or NFS mount, or NVMe) through which hosts reach vVols |
| vVol objects | config, data (one per VMDK), swap, memory (snapshot) |

## Deploy
1. Array: enable vVols, create a storage container, configure PE access for every host
   (iSCSI/FC zoning or NFS export as for any datastore).
2. vCenter → Configure → Storage Providers → Add: VASA URL and credentials (check the
   certificate trust; VASA 3+/4 uses vCenter-issued or CA certs).
3. New Datastore → vVol → pick the container; mount to all hosts.
4. Create VM storage policies using the array's capabilities (replication, snapshot
   schedules, QoS); assign at VM creation.

## Operating
- **Snapshots** are array-native (offloaded), so deleting them does not cause the
  consolidation storms of VMFS snapshots.
- Storage vMotion between vVol and VMFS works; between arrays it is a full copy.
- **VASA is the control plane:** if unavailable, running VMs keep doing I/O, but power-on,
  snapshot, create and some HA restarts fail. Make the VASA provider highly available and
  monitor its certificate expiry.

## Gotchas
- vCenter restore or certificate regeneration may require re-registering VASA.
- Backup software must support vVols (VADP works; check array-specific integrations).
- Each vVol counts against array object limits; snapshot-heavy schedules hit them first.

## Verify
`esxcli storage vvol vasaprovider list` shows the provider online; `esxcli storage vvol
protocolendpoint list` shows PEs accessible from every host; policy compliance is green.
