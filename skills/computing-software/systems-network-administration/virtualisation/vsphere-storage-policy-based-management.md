---
id: computing-software.systems-network-administration.virtualisation.vsphere-storage-policy-based-management
name: vsphere-storage-policy-based-management
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [spbm, vm-storage-policy, storage-policy, tag-based-placement, vsan, vvols, vsphere-storage, storage-compliance, vmware, vsphere]
level: practitioner
status: draft
description: "Use vSphere storage policies (SPBM): tag-based placement on VMFS/NFS, vSAN and vVols rules, assigning per-disk policies, compliance checks and reapplying after changes."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage Policy Based Management (SPBM)

**Goal:** VMs land on storage that meets their service level, and you can prove it with a
compliance check instead of a spreadsheet.

## Policy types
| Rule set | Works with | Example |
|---|---|---|
| Tag-based placement | VMFS, NFS datastores tagged in vCenter | Category "StorageTier": Gold/Silver |
| vSAN | vSAN datastores | FTT=1 RAID-1, stripe width, encryption, space efficiency |
| vVols (VASA provider) | vVols arrays | replication groups, dedupe, QoS exposed by the array |
| Host-based (VAIO) | any | VM encryption, Storage I/O Control |

## Tag-based tiers
1. Tags & Custom Attributes → category `StorageTier` (one tag per object), tags
   Gold/Silver/Bronze.
2. Tag each datastore (or datastore cluster).
3. Policies and Profiles → VM Storage Policies → Create → "Enable tag based placement
   rules" → Use storage tagged with Gold.
4. At VM creation pick the policy; the datastore list filters to compatible ones.

## Assign and check
- Policies apply per VM home and **per virtual disk**; a DB VM can have its log disk on
  a different tier.
- Changing a policy definition marks VMs "Out of date"; **Reapply** VM storage policy.
  On vSAN this can trigger large resync traffic, so reapply in batches.
- Compliance: VM → Configure → Policies → Check Compliance, or for the estate:
```powershell
Get-SpbmEntityConfiguration -VM (Get-VM) | Where ComplianceStatus -ne 'compliant'
Set-SpbmEntityConfiguration -Configuration (Get-SpbmEntityConfiguration (Get-VM web01)) -StoragePolicy (Get-SpbmStoragePolicy Gold)
```

## Gotchas
- Default policy per datastore (vSAN Default Storage Policy) is used when none is
  selected; change it deliberately, not by accident.
- Moving a VM with Storage vMotion to a non-compatible datastore leaves it
  non-compliant silently unless you check.
- Tags are vCenter objects: a restored or rebuilt vCenter without tags loses placement
  logic.

## Verify
A report of non-compliant VMs is empty (or each exception is documented), and new VMs
pick the intended default policy.
