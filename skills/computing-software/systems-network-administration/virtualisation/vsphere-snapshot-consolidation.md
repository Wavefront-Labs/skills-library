---
id: computing-software.systems-network-administration.virtualisation.vsphere-snapshot-consolidation
name: vsphere-snapshot-consolidation
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [snapshot-consolidation, delta-disk, snapshot, consolidation-needed, vmsd, sesparse, snapshot-report, vsphere-vm-administration, vmware, vsphere]
level: practitioner
status: draft
description: "Handle vSphere snapshots: find old ones, delete safely, fix 'consolidation needed', locked delta files from backup proxies, and recover a broken snapshot chain."
sources:
  - https://knowledge.broadcom.com/external/article?legacyId=1025279
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vSphere snapshot management and consolidation

**Goal:** no stale snapshots, and when deleting one fails, fix it without corrupting the
VM's disks.

## Find them
```powershell
Get-VM | Get-Snapshot | Where Created -lt (Get-Date).AddDays(-3) |
  Select VM, Name, Created, @{n='GB';e={[math]::Round($_.SizeGB,1)}} | Sort GB -Desc
Get-VM | Where {$_.ExtensionData.Runtime.ConsolidationNeeded}
```
Files: `<vm>-00000N.vmdk` + `-sesparse.vmdk` (VMFS6, SEsparse) or `-delta.vmdk`;
the snapshot tree lives in `<vm>.vmsd`.

## Delete safely
- **Delete** (or Delete All) merges deltas into the base; I/O heavy, run off-hours for big
  ones. Needs free space on the datastore for the merge in some cases.
- Very large snapshots: shutting down the VM makes the merge faster and avoids stun.
- In vSphere 6.0+ consolidation uses a mirror driver and is much less disruptive, but a
  final brief stun still occurs.

## "Virtual machine disks consolidation is needed"
The snapshot manager shows nothing but delta files remain (a delete failed midway).
VM → Snapshots → **Consolidate**. If it fails with "file locked":
1. A backup proxy still has the delta **hot-added**: in the proxy VM's settings, remove
   the stray disk (do not delete from disk), then retry.
2. Find the lock holder: `vmkfstools -D <file>-000001-sesparse.vmdk` and look up the owner
   MAC in `vmkernel.log`, or restart management agents on the host holding it.
3. Retry Consolidate.

## Broken chain (last resort)
Symptoms: VM won't power on, "parent disk modified". Do not edit descriptor CIDs by
hand unless you know the chain; clone the VM's current state (`vmkfstools -i
<vm>-00000N.vmdk new.vmdk`) to a new disk first so you have a copy, then open a support
case. Restore from backup is often faster.

## Prevention
- Alarm on snapshot age and on "VM consolidation needed" status.
- Backup software should clean up its own snapshots; alert on snapshots named like
  "VEEAM BACKUP TEMPORARY SNAPSHOT" older than a day.

## Verify
Snapshot report is empty beyond policy; no VMs flagged for consolidation; datastore free
space recovered after deletes.
