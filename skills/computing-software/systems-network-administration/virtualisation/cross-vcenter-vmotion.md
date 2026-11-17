---
id: computing-software.systems-network-administration.virtualisation.cross-vcenter-vmotion
name: cross-vcenter-vmotion
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vmotion, cross-vcenter-vmotion, xvc-vmotion, advanced-cross-vcenter-vmotion, move-vm, vcenter-migration, long-distance-vmotion, vmware, vsphere]
level: advanced
status: draft
description: "Move running VMs between vCenters: linked-mode xVC-vMotion, Advanced Cross vCenter vMotion without linking, Move-VM in PowerCLI, network/EVC prerequisites and rollback."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-vCenter vMotion

**Goal:** migrate live VMs between vCenter instances (new hardware, new vCenter, data
centre move) without downtime or re-IP.

## Variants
| Variant | Needs | Use |
|---|---|---|
| Cross vCenter vMotion (ELM) | Both vCenters in the same SSO domain | Day-to-day moves between linked vCenters |
| **Advanced Cross vCenter vMotion (XVM)** | vCenter 7.0U1c+, no linking; source credentials entered in the target client | Migrating to a new vCenter/SSO domain, consolidations |
| PowerCLI `Move-VM` across `Connect-VIServer` sessions | Same API underneath | Bulk and scripted moves |

## Prerequisites
- vMotion networks routable between source and destination hosts (use the vMotion
  TCP/IP stack with gateways), ≤150 ms RTT, 250 Mbps+ per concurrent migration.
- Destination port group exists with the same VLAN (name may differ; map in the wizard).
- CPU compatibility: destination EVC baseline ≥ the VM's current feature set; VMs with
  per-VM EVC can move between differing clusters.
- Storage: shared storage not required; it performs vMotion + Storage vMotion together
  (longer for large disks).
- Matching or newer ESXi on destination; VM hardware version supported there.

## PowerCLI bulk example
```powershell
$src = Connect-VIServer old-vc ; $dst = Connect-VIServer new-vc
$vm  = Get-VM app01 -Server $src
$pg  = Get-VDPortgroup -Name 'VM-App-120' -Server $dst
Move-VM -VM $vm -Destination (Get-VMHost esx-n01 -Server $dst) `
        -Datastore (Get-Datastore ds-n01 -Server $dst) `
        -NetworkAdapter (Get-NetworkAdapter -VM $vm) -PortGroup $pg
```

## Gotchas
- vDS port groups: the VM keeps its MAC; destination vCenter may flag duplicates if
  ranges overlap (MAC allocation per vCenter instance ID); give vCenters unique instance
  IDs.
- Tags, custom attributes, DRS rules, folders and permissions do **not** move; script
  them separately.
- Backup jobs reference the source vCenter object IDs; rebuild job membership after.
- VMs with snapshots, RDMs or attached ISOs on local storage often fail the check.

## Verify
Compatibility check in the wizard is green before launch; after migration the VM keeps
pinging throughout (one lost packet at most), and inventory, tags and backup jobs are
reconciled.
